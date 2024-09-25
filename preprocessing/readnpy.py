import numpy as np


P = np.load("signature/1.npy")
C = np.load("signature/2.npy")
P = P[:,np.newaxis]
C = C[:,np.newaxis]
signature_averge = np.hstack((C,P))
np.save("signature/signature_averge.npy", signature_averge)

