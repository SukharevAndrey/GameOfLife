import numpy as np


class Life:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.prev_prev_world = np.zeros((m, n))
        self.prev_world = np.zeros((m, n))
        self.world = np.zeros((m, n))
        self.lifetime = np.zeros((m, n))
        self.underpop = 2
        self.overcrowd = 3
        self.reproduction = 3
        self.wrap = True

    def random_populate(self, w_chance, b_chance):
        self.world = np.random.choice([0, 1], self.m * self.n, p=[w_chance, b_chance]).reshape(self.m, self.n)

    def populate_from_file(self, filename):
        with open(filename) as f:
            s = f.readline()
            m, n = map(int, s.split())
            w = np.zeros((m, n))
            wrap_mode = f.readline()
            for i in range(m):
                s = f.readline()
                for j in range(n):
                    w[i, j] = 1 if s[j] == '*' else 0
            self.world = w
            self.lifetime = np.zeros((m, n))
            self.wrap = True if wrap_mode == 'T' else False
            self.m = m
            self.n = n

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.m) + ' ' + str(self.n) + '\n')
            f.write('T\n' if self.wrap else 'F\n')
            f.write('\n'.join(''.join('*' if self.world[i, j] else '.' for j in range(self.n)) for i in range(self.m)))

    def clear_world(self):
        self.prev_prev_world = np.zeros((self.m, self.n))
        self.prev_world = np.zeros((self.m, self.n))
        self.world = np.zeros((self.m, self.n))
        self.lifetime = np.zeros((self.m, self.n))

    def toggle_wrapping(self):
        self.wrap = not self.wrap

    def extend_world(self, delta_m, delta_n):
        if delta_m > 0:
            self.world = np.concatenate((self.world, np.zeros((delta_m, self.n))))
        elif delta_m < 0:
            self.world = self.world[:self.m + delta_m, :]
        self.m += delta_m
        if delta_n > 0:
            self.world = np.concatenate((self.world, np.zeros((self.m, delta_n))), axis=1)
        elif delta_n < 0:
            self.world = self.world[:, :self.n + delta_n]
        self.n += delta_n

    def neighbors_count(self, i, j):
        if self.wrap:
            neighbors = sum(self.world[a, b] for a in ((i - 1) % self.m, i, (i + 1) % self.m) \
                            for b in ((j - 1) % self.n, j, (j + 1) % self.n)) - self.world[i, j]
        else:
            neighbors = 0
            if i - 1 > 0:
                neighbors += self.world[(i - 1), j]
                if j - 1 > 0:
                    neighbors += self.world[(i - 1), (j - 1)]
                if j + 1 < self.n:
                    neighbors += self.world[(i - 1), (j + 1)]
            if i + 1 < self.m:
                neighbors += self.world[(i + 1), j]
                if j - 1 > 0:
                    neighbors += self.world[(i + 1), (j - 1)]
                if j + 1 < self.n:
                    neighbors += self.world[(i + 1), (j + 1)]
            if j - 1 > 0:
                neighbors += self.world[i, (j - 1)]
            if j + 1 < self.n:
                neighbors += self.world[i, (j + 1)]
        return neighbors

    def evolve(self):
        new_world = self.world.copy()
        for i in range(self.m):
            for j in range(self.n):
                neighbors = self.neighbors_count(i, j)
                if self.world[i, j]:
                    if neighbors < self.underpop or neighbors > self.overcrowd:
                        new_world[i, j] = 0
                        self.lifetime[i, j] = 0
                    else:
                        self.lifetime[i, j] += 1
                else:
                    if neighbors == self.reproduction:
                        new_world[i, j] = 1
                        self.lifetime[i, j] = 1

        self.prev_prev_world = self.prev_world
        self.prev_world = self.world
        self.world = new_world
        if np.all(self.world == self.prev_prev_world):
            return False
        else:
            return True