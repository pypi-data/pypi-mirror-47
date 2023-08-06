import pandas as pd

from featuretoolsOnSpark.tableset import TableSet
from collections import defaultdict
import featuretoolsOnSpark.column_types as ctypes
from pyspark.sql.functions import *
import time,logging

logging.basicConfig(format = '%(module)s-%(levelname)s- %(message)s')
logger = logging.getLogger('featuretoolsOnSpark')
logger.setLevel(20)

def dfs(tableset=None,
        target_table=None,
        agg_primitives=None,
        allowed_paths=None,
        max_depth=2,
        ignore_tables=None,
        ignore_columns=None,
        verbose=True):
    '''Calculates features given a tableset.

    Args:

        tableset (TableSet): An already initialized tableset. Required if
            tables and relationships are not defined.

        target_table (str): Table id of table on which to make predictions.

        agg_primitives (list[str], optional): List of Aggregation
            Feature types to apply.

                Default: ['avg','count','kurtosis','skewness','stddev','min','max','sum']

        allowed_paths (list[list[str]]): Allowed table paths on which to make
            features.

        max_depth (int) : Maximum allowed depth of features.

        ignore_tables (list[str], optional): List of tables to
            blacklist when creating features.

        ignore_columns (dict[str -> list[str]], optional): List of specific
            columns within each table to blacklist when creating features.

        verbose(bool) : Whether to display information

        Example:
        for Kaggle Competition Home Credit Default Risk Dataset(https://www.kaggle.com/c/home-credit-default-risk/data)

            all_features=fts.dfs(tableset = ts, agg_primitives=["sum",'min','max','avg','stddev'],target_table = 'app_train',max_depth=2)

    '''
    if not isinstance(tableset, TableSet):
        tableset = TableSet("dfs")
    start=time.time()
    dfs_object = DeepFeatureSynthesis(target_table, tableset,
                                      agg_primitives=agg_primitives,
                                      max_depth=max_depth,
                                      allowed_paths=allowed_paths,
                                      ignore_tables=ignore_tables,
                                      ignore_columns=ignore_columns,
                                      verbose=verbose)

    dfs_object.build_features(verbose=verbose)
    end=time.time()
    if verbose:
        logger.info("All DFS Time:{:.3f}s".format(end-start))


class DeepFeatureSynthesis(object):
    """Automatically produce features for a target table in an Tableset.

        Args:
            target_table_id (str): Id of table for which to build features.

            tableset (TableSet): Tableset for which to build features.

            agg_primitives (list[str], optional):
                list of Aggregation Feature types to apply.

                Default: ['avg','count','kurtosis','skewness','stddev','min','max','sum']

            max_depth (int, optional) : maximum allowed depth of features.
                Default: 2. If -1, no limit.

            allowed_paths (list[list[str]], optional): Allowed table paths to make
                features for. If None, use all paths.

            ignore_tables (list[str], optional): List of tables to
                blacklist when creating features. If None, use all tables.

            ignore_columns (dict[str -> list[str]], optional): List of specific
                columns within each table to blacklist when creating features.
                If None, use all columns.

            verbose(bool) : Whether to display information
        """

    def __init__(self,
                target_table_id,
                tableset,
                agg_primitives=None,
                max_depth=2,
                allowed_paths=None,
                ignore_tables=None,
                ignore_columns=None,
                verbose=True):

        if target_table_id not in tableset.table_dict:
            ts_name = tableset.id or 'table set'
            msg = 'Provided target table %s does not exist in %s' % (target_table_id, ts_name)
            raise KeyError(msg)

        self.verbose = verbose
        # need to change max_depth to None because DFs terminates when  <0
        if max_depth is not None:
            assert max_depth>0,"max_depth must be greater than 0"
        self.max_depth = max_depth

        self.allowed_paths = allowed_paths
        if self.allowed_paths:
            self.allowed_paths = set()
            for path in allowed_paths:
                self.allowed_paths.add(tuple(path))

        if ignore_tables is None:
            self.ignore_tables = set()
        else:
            if not isinstance(ignore_tables, list):
                raise TypeError('ignore_tables must be a list')
            assert target_table_id not in ignore_tables,\
                "Can't ignore target_table!"
            self.ignore_tables = set(ignore_tables)

        self.ignore_columns = defaultdict(set)
        if ignore_columns is not None:
            for eid, vars in ignore_columns.items():
                self.ignore_columns[eid] = set(vars)
        self.target_table_id = target_table_id
        self.ts = tableset

        if agg_primitives is None:
            agg_primitives = ['avg','count','kurtosis','skewness','stddev','min','max','sum']
        self.agg_primitives = []
        agg_prim_default = ['avg','count','kurtosis','skewness','stddev','min','max','sum']
        for a in agg_primitives:
            if isinstance(a,str):
                if a.lower() not in agg_prim_default:
                    raise ValueError("Unknown aggregation primitive {}. ".format(a))
            self.agg_primitives.append(a.lower())

        if self.verbose:
            logger.info(("using agg_primitives:",self.agg_primitives))
    
    def build_features(self, verbose=False):
        """Automatically builds feature definitions for target
            table using Deep Feature Synthesis algorithm

        Args:
            verbose (bool, optional): If True, print progress.

        Returns:
            dataframe: return new dataframe of target table
        """
        all_features = {}
        for e in self.ts.tables:
            if e not in self.ignore_tables:
                all_features[e.id] = {}

        self._run_dfs(self.ts[self.target_table_id], [], all_features, max_depth=self.max_depth)

        start = time.time()
        new_cols = []
        for col in self.ts[self.target_table_id].df.columns:
            if col.find('(') > -1:
                new_col = col.replace('(','_')
                new_col = new_col.replace(')','')
            else:
                new_col = col
            new_cols.append(new_col)
        rename_expr = [" `"+i+"`"+" as "+"`"+j+"` " for i, j in zip(self.ts[self.target_table_id].df.columns, new_cols)]
        self.ts[self.target_table_id].df = self.ts[self.target_table_id].df.selectExpr(rename_expr)

        end = time.time()
        if self.verbose:
            logger.info(" change features time:{:.3f}s".format(end-start))

    
    def _run_dfs(self, table, table_path, all_features, max_depth):
        """
        create features for the provided table

        Args:
            table (Table): Table for which to create features.
            table_path (list[str]): List of table ids.
            all_features (dict[Table.id -> dict[str -> Column]]):
                Dict containing a dict for each table. Each nested dict
                has features as values with their ids as keys.
            max_depth (int) : Maximum allowed depth of features.
        """
        if max_depth is not None and max_depth < 0:
            return

        table_path.append(table.id)
        """
        Step 1 - Recursively build features for each table in a backward relationship
        """
        backward_tables = self.ts.get_backward_tables(table.id)
        backward_tables = [b_id for b_id in backward_tables if b_id not in self.ignore_tables]
        for b_table_id in backward_tables:
            # if in path, we've already built features
            if b_table_id in table_path:
                continue

            if self.allowed_paths and tuple(table_path + [b_table_id]) not in self.allowed_paths:
                continue
            new_max_depth = None
            if max_depth is not None:
                new_max_depth = max_depth - 1
            self._run_dfs(table=self.ts[b_table_id],table_path=list(table_path),all_features=all_features,max_depth=new_max_depth)

        """
        Step 2 - Create agg_feat features for all deep backward relationships
        """
        backward = [r for r in self.ts.get_backward_relationships(table.id)
                   if r.child_table.id in backward_tables and
                   r.child_table.id not in self.ignore_tables]
        for r in backward:
            if self.allowed_paths and tuple(table_path + [r.child_table.id]) not in self.allowed_paths:
                continue
            start = time.time()
            self._build_agg_features(r=r,
                                     all_features=all_features,
                                     max_depth=max_depth)
            end = time.time()
            if self.verbose:
                logger.info(r.parent_table.id+" "+r.child_table.id+" build agg features time:{:.3f}s".format(end-start))

        """
        Step 3 - Add all features
        """
        self._add_all_features(all_features, table)

    def _build_agg_features(self, r, all_features, max_depth=0):
        if max_depth is not None and max_depth < 0:
            return

        new_max_depth = None
        if max_depth is not None:
            new_max_depth = max_depth - 1

        input_types = "numeric"

        features = self._features_by_type(all_features=all_features,
                                            table=r.child_table,
                                            max_depth=new_max_depth,
                                            column_type=input_types)

        # remove features in relationship path
        relationship_path = self.ts.find_backward_path(self.target_table_id, r.child_table.id)

        features = [f for f in features if not self._feature_in_relationship_path(relationship_path, f)]
        _local_data_stat_df = None

        if self.verbose:
            logger.info(r.parent_table.id+" "+r.child_table.id+" select {} features.".format(len(features)))
        start = time.time()
        group_all = list()  
        group_all.append(r.child_column.id) 
        features_prim = []
        for agg_prim in self.agg_primitives:

            features_prim +=[agg_prim+"(\""+f.id+"\")" for f in features]
            
        _local_data_stat_df = r.child_table.df.groupby(group_all).agg(*[eval(f) for f  in features_prim])
        end =time.time()

        if self.verbose:
            logger.info(r.parent_table.id+" "+r.child_table.id+" agg_features time:{:.3f}s".format(end-start))

        start = time.time()
        new_cols = []
        for column in _local_data_stat_df.columns:
            if column in group_all:
                new_cols.append(column)
                continue
            index = column.find('(')
            new_col = column[:index+1]+r.child_table.id+'_'+column[index+1:]
            new_cols.append(new_col)

            _c = ctypes.Numeric(new_col, r.parent_table)
            all_features[r.parent_table.id][new_col] = _c
            r.parent_table.columns += [_c]

        rename_expr = [" `"+i+"`"+" as "+"`"+j+"` " for i, j in zip(_local_data_stat_df.columns, new_cols)]
        _local_data_stat_df = _local_data_stat_df.selectExpr(rename_expr)
        end =time.time()
        if self.verbose:
            logger.info(r.parent_table.id+" "+r.child_table.id+" add columns time:{:.3f}s".format(end-start))

        start = time.time()
        r.parent_table.df = r.parent_table.df.join(_local_data_stat_df,\
            r.parent_table.df[r.parent_column.id]==_local_data_stat_df[r.child_column.id],how='left_outer')

        for col in group_all:
            r.parent_table.df = r.parent_table.df.drop(_local_data_stat_df[col])
        end =time.time()
        if self.verbose:
            logger.info(r.parent_table.id+" "+r.child_table.id+" join parent table time:{:.3f}s".format(end-start))

    def _add_all_features(self, all_features, table):
        """add all columns from the given table into features

        Args:
            all_features (dict[Table.id -> dict[str -> Column]]):
                Dict containing a dict for each table. Each nested dict
                has features as values with their ids as keys.
            table (Table): Table to calculate features for.
        """
        columns = table.columns
        ignore_columns = self.ignore_columns[table.id]
        for v in columns:
            if v.id in ignore_columns:
                continue
            all_features[table.id][v.id]=v

    def _features_by_type(self, all_features, table, max_depth,
                          column_type=None):

        selected_features = []

        if max_depth is not None and max_depth < 0:
            return selected_features

        for feat in all_features[table.id]:
            f = all_features[table.id][feat]
            if f.dtype == column_type:
                selected_features.append(f)

        return selected_features

    def _feature_in_relationship_path(self, relationship_path, feature):

        for relationship in relationship_path:
            if  relationship.child_column.id == feature.id or relationship.parent_column.id == feature.id:
                return True
        return False
        