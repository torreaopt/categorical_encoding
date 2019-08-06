from .encoder_methods import BinaryEncoder, HashingEncoder, OrdinalEncoder


class Encoder():
    def __init__(self, method=OrdinalEncoder, to_encode=None, top_n=10):
        encoder_list = {'ordinal': OrdinalEncoder,
                        'binary': BinaryEncoder,
                        'hashing': HashingEncoder}
        if method in encoder_list:
            method = encoder_list[method]

        self.method = method(cols=to_encode)
        # top_n only for OneHotEncoder
        self.top_n = top_n
        self.features = []

    def fit(self, X, y=None):
        self.method.fit(X, y)
        return self

    def transform(self, X, features):
        self.features = features
        self._encode_features_list(X)
        return self.method.transform(X, self.features)

    def fit_transform(self, X, features, y=None):
        return self.fit(X, y).transform(X, features)

    def get_features(self):
        return self.features

    def get_mapping(self, category=0):
        return self.method.get_mapping(category)

    def get_hash_method(self):
        if not isinstance(self.method, HashingEncoder):
            raise TypeError("Must be HashingEncoder")
        return self.method.hash_method

    def get_n_components(self):
        if not isinstance(self.method, HashingEncoder):
            raise TypeError("Must be HashingEncoder")
        return self.method.n_components

    def _encode_features_list(self, X):
        self.features = self.method.encode_features_list(X, self.features)