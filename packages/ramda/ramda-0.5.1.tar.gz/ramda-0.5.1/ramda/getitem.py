from ramda.curry import curry


getitem = curry(lambda key, collection: collection[key])
