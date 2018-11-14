

class Evaluation:
    def __init__(self):
        self.w = 0
        self.W = 0
        self.D = 0
        self.L = 0
        self.n = 0

    def update(self, n, w, W, D, L):
        self.w += w
        self.W += W
        self.D += D
        self.L += L
        self.n += n
        
    def done(self):
        self.w /= self.n
        
    def __str__(self):
        return "w = %.4f W = %.3f D = %.3f L = %.3f n = %.3f" % (self.w, self.W, self.D, self.L, self.n)

