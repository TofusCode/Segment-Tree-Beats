import sys
from math import ceil, log2
input = sys.stdin.readline
inf = float('inf')

class SegTreeBEATS:
    def __init__(self, n, a):
        self.size = 1 << ceil(log2(n))
        self.a = a
        # node has [max_val, max_cnt, smax_val, sum]
        self.tree = [[-inf, 0, -inf, 0] for _ in range(2*self.size)]
        self.build(1, 0, n-1)
    
    def build(self, i, start, end):
        if start == end:
            self.tree[i] = [self.a[start], 1, -inf, self.a[start]]
        else:
            self.build(i*2, start, (start+end)//2)
            self.build(i*2+1, (start+end)//2+1, end)
            self.tree[i] = self.merge(self.tree[2*i], self.tree[2*i+1])

    def merge(self, a, b):
        # max_val is same
        # a.max_val, a.max_cnt + b.max_cnt, max(a.smax_val, b.smax_val), a.sum + b.sum
        if a[0] == b[0]:
            return [a[0], a[1]+b[1], max(a[2], b[2]), a[3]+b[3]]
        # a.max_val < b.max_val
        if a[0] < b[0]:
            a, b = b, a
        # a.max_val, a.max_cnt, max(b.max_val, a.smax_val), a.sum + b.sum
        # a.max_val >= b.max_val ? a.smax_val -> smax_val = max(b.max_val, a.smax_val)
        return [a[0], a[1], max(b[0], a[2]), a[3]+b[3]]
    
    def propagate(self, i):
        if i < self.size:
            for j in [2*i , 2*i+1]:
                if self.tree[i][0] < self.tree[j][0]:
                    #tree[j].sum -= (tree[j].max_val - tree[i].max_val) * tree[j].max_cnt
                    #tree[j].max_val = tree[i].max_val
                    self.tree[j][3] -= (self.tree[j][0] - self.tree[i][0])*self.tree[j][1]
                    self.tree[j][0] = self.tree[i][0]

    # i = current node // start, end = node interval // left, right = query range // diff = update value
    def update(self, i, start, end, left, right, diff):
        self.propagate(i)
        # case 1 (break): out of range or max_val <= X
        if (right < start) or (end < left) or (self.tree[i][0] <= diff):
            return
        # case 2 (tag): smax_val < X < max_val
        if left <= start and end <= right and self.tree[i][2] <= diff:
            # tree[i].sum -= (tree[i].max_val - val) * tree[i].max_cnt
		    # tree[i].max_val = val
            # only all max_val is change, so max_cnt remains
            self.tree[i][3] -= (self.tree[i][0] - diff)*self.tree[i][1]
            self.tree[i][0] = diff
            self.propagate(i)
            return
        
        self.update(2*i, start, (start + end)//2, left, right, diff)
        self.update(2*i+1, (start + end)//2+1, end, left, right, diff)
        self.tree[i] = self.merge(self.tree[2*i], self.tree[2*i+1])

    def querySum(self, i, start, end, left, right):
        self.propagate(i)
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[i][3]
        lsum = self.querySum(2*i, start, (start + end)//2, left, right)
        rsum = self.querySum(2*i+1, (start + end)//2+1, end, left, right)
        return lsum + rsum

    def queryMax(self, i, start, end, left, right):
        self.propagate(i)
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[i][0]
        lmax = self.queryMax(2*i, start, (start + end)//2, left, right)
        rmax = self.queryMax(2*i+1, (start + end)//2+1, end, left, right)
        return max(lmax, rmax)


n = int(input())
a = list(map(int, input().split()))

tree = SegTreeBEATS(n, a)
for _ in range(int(input())):
    what, *q = map(int, input().split())
    if what == 1:
        L, R, X = q
        tree.update(1, 0, n-1, L-1, R-1, X)
    elif what == 2:
        L, R = q
        print(tree.queryMax(1, 0, n-1, L-1, R-1))
    else:
        L, R = q
        print(tree.querySum(1, 0, n-1, L-1, R-1))