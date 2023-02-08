import matplotlib.pyplot as plt

class plot:
    def __init__(self):
        self.vel_list = [0]
        self.height_list = [0]
        self.time_list = [0]

    def show(self, data):
        print(data[0])
        self.vel_list.append(data[0])
        self.height_list.append(data[1])
        self.time_list.append(data[2])

        plt.plot(self.time_list, self.vel_list, label="velocity")
        plt.plot(self.time_list, self.height_list, label="height")
        plt.xlabel('Time')
        plt.ylabel('Height / Velocity')
        plt.title('Graph')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    p = plot()
    p.show([2, 3, 1])
    p.show([1, 2, 1.1])
    p.show([5, 1, 2])
