import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("plot.csv", header = 0)

time = df.Time.to_list()
sheep = df.Sheep.to_list()
wolves = df.Wolves.to_list()
grass = df.Grass.to_list()
dirt = df.Dirt.to_list()

plt.plot(time, sheep, label = "Sheep", linestyle="-")
plt.plot(time, wolves, label = "Wolves", linestyle="--")
plt.plot(time, grass, label = "Grass/5", linestyle="-.")
plt.plot(time, dirt, label = "Dirt/5", linestyle="-.")
plt.legend()
plt.title("Wolves-Sheep-Grass")
plt.savefig("WSGplot.png")
plt.show()