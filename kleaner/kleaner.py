import numpy as np
import pandas as pd


class Kleaner(pd.DataFrame):
    """
    A class to allow people to decide how to clean data

    # Usage:

        k = Kleaner(pd.DataFrame(...))

        # analyze a list of column cleaniness
        k = healthiness()

    """
    ID_TYPE = 'id'
    SCALE_TYPE = 'scale'
    FLAG_TYPE = 'flag'
    OBJECT_FLAG_TYPE = 'object_flag'
    BINARY_FLAG = 'binary_flag'
    NEED_EXTRACTION = 'extraction'
    SPARSE = 'sparse'

    NORMALIZE_FIRST_LETTER = 'first_letter'
    NORMALIZE_SIZE = 'size'

    def __init__(self, df, target_column=None):
        super(Kleaner, self).__init__(df)
        self.type = None  # self.guess_type(self.columns)
        self.target_column = target_column

    @property
    def scalar_columns(self):
        """
        Return a list of columns which are suitably scalar :)
        """
        return [
            col
            for col, typ in self.dtypes.iteritems()
            if (
                typ.name.startswith(('int', 'float'))
                and col != self.target_column
            )
        ]

    def healthiness(self):
        """
        We have a few metrics of the definitions

        Measure we calculate:
        * Completeness - Referring to missing key information
            - % of nulll values of a column
        * Consistency - Referring to single representation of data  
            - % of diversity of value

        * Accuracy - Referring to the level that data is accurately represented
        * Integrity - Referring to data relations when a broken link is presented
        * Validity - Referring to data format & valid values
        * Timeliness - How to deal with data timing?
        * Currency - Referring to degree of data current with the world
        """
        return {
            c: self.get_col_health(c)
            for c in df.columns
        }

    def get_col_health(self, c):
        round_to_2 = lambda x: float("{:.2f}".format(x))
        MAX_VALUE_COUNT = 6
        return {
            'completeness': round_to_2(100. * (len(self) - self[c].isnull().sum()) / len(self)),
            # Anything above 6 items should be 0, anything below should be
            'consistency': 100. * max((MAX_VALUE_COUNT + 1 - self[c].nunique()), 0) / MAX_VALUE_COUNT
        }

    def guess_type(self):
        return {
            c: self.guess_type_col(c)
            for c in df.columns
        }

    def guess_type_col(self, c, threshold=0.2):
        """
        Different types:

        id_field: int and not consistent
        scale_field: float and not consistent
        flag_field: int and consistent
        need_conversion_flag_field: object and consistent
        """
        col_health = self.get_col_health(c)
        col_type = self[c].dtype.name
        if col_health['completeness'] < threshold:
            return self.SPARSE
        elif col_health['consistency'] < threshold:
            return self.ID_TYPE
        elif col_type.startswith(('int', 'float')):
            return self.FLAG_TYPE
        elif self[c].nunique() <= 2:
            return self.BINARY_FLAG
        elif col_type.startswith('object'):
            return self.OBJECT_FLAG_TYPE
        return None

    def normalize_cols(self, cs=None, postfix='_normalized'):
        if cs is None:
            cs = [c for c in self.columns if self.guess_type_col(
                c) == self.BINARY_FLAG]
        for c in cs:
            self[c + postfix] = self.normalize_col(c)
        return self

    def normalize_col(self, c, method=None):
        col_type = self.guess_type_col(c)
        if col_type == self.BINARY_FLAG:
            values = self[c].dropna().unique()
            # XXX: sorted so yes will be returned 1
            mapper = {v: i for i, v in enumerate(sorted(values))}
            f_convert = lambda x: mapper[x] if pd.notnull(x) else 0
            return self[c].apply(f_convert)
        elif method == self.NORMALIZE_FIRST_LETTER:
            values = {v[0] for v in self[c].dropna().unique()}
            # XXX: sorted so yes will be returned 1
            mapper = {v: i for i, v in enumerate(sorted(values))}
            f_convert = lambda x: mapper[x[0]] if pd.notnull(x) else 0
            return self[c].apply(f_convert)
        elif method == self.NORMALIZE_SIZE:
            config = {
                'large': 10,
                'high': 10,
                'med': 5,
                'small': 3,
                'compact': 2,
                'low': 1,
                'mini': 1
            }
            f_convert = lambda x: [score for s, score in config.items() if s in x.lower()][
                0] if pd.notnull(x) else 0
            return self[c].apply(f_convert)

        raise NotImplementedError("Not know how to normalize {}".format(c))
