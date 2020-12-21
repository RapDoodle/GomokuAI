"""For testing only"""

from nn.model import SequentialModel
from nn.layers import Input, Dense, Output

import numpy as np

import nn.math as m

model = SequentialModel()
model.add(Input(4))
model.add(Dense(6, activation = 'sigmoid', use_bias = True))
model.add(Dense(3, activation = 'sigmoid', use_bias = True))
model.add(Dense(2, activation = 'sigmoid', use_bias = True))
model.add(Output(1, activation = 'sigmoid', use_bias = True))
model.compile()
model.summary()
print(model.predict(np.array([1, 2, 3, 4]).reshape(4,1)))
model.fit(np.array([1, 2, 3, 4]).reshape(4,1), np.array([1]).reshape(1,1))

from gomoku.message_box import info_message_box
info_message_box('Done')