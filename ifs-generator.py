"""
Licensed under CC-BY-NC-ND (Creative Commons Non-Commercial No-Derivatives License)

https://creativecommons.org/licenses/by-nc-nd/4.0/

Copyright Scott Morgan 2022

"""
import matplotlib.pyplot as plt
import numpy as np
import json
import glob

def main():

  file_list = glob.glob("*.json")
  if not file_list:
    raise FileNotFoundError('JSON file not found. Please ensure your JSON file is in the same directory as this Python file.')
  else:
    file_name = file_list[0]
    dotcolor, facecolor, rd_seed_init = read_json_file(file_name)
    
  x, y, rd_seed = run_program(rd_seed_init)
  write_image_file(x,y,rd_seed,dotcolor,facecolor)

def read_json_file(file_name):

  with open(file_name, "r") as read_file:
    data = json.load(read_file)
    facecolor = data["background_color"]
    dotcolor = data["attributes"][0]["dot_color"]
    (rnd0,rnd1,rnd2,rnd3,rnd4) = data["attributes"][0]["random_seed"]
    rd_seed_init = (rnd0,rnd1,rnd2,rnd3,rnd4)

  return dotcolor, facecolor, rd_seed_init

def write_image_file(x,y,rd_seed,dotcolor,facecolor):

  fig1 = plt.figure(1,figsize=(66.25,46.75))
  ax1 = plt.axes()
  ax1.scatter(x, y, s = 100.0, color=dotcolor, edgecolors='none')
  ax1.axis('off')
  ax1.add_patch(plt.Rectangle((0,0), 1, 1, facecolor=facecolor,transform=ax1.transAxes, zorder=-1))

  filename_png = "output.png"
  plt.savefig(filename_png)

def run_program(rd_seed_init):

  x, y = [0], [0]
  rd_seed = rd_seed_init
  np.random.set_state(rd_seed_init)

  e, f = np.random.uniform(-1,1), np.random.uniform(-1,1)

  while True:
    cont = 0
    a, b = np.random.uniform(-1,1,size=4), np.random.uniform(-1,1,size=4)
    c, d = np.random.uniform(-1,1,size=4), np.random.uniform(-1,1,size=4)

    for iter in range(4):
      if (a[iter]**2 + c[iter]**2 < 1) and (b[iter]**2 + d[iter]**2 < 1) and (a[iter]**2 + b[iter]**2 + c[iter]**2 + d[iter]**2 < 1 + (a[iter]*d[iter] - c[iter]*b[iter])**2):
        cont += 1

    if cont == 4:
      break

  for i in range(100000):

    ni = np.random.randint(0,4)

    x.append(a[ni]*x[i] + b[ni]*y[i]+e)
    y.append(c[ni]*x[i] + d[ni]*y[i]+f)

  return x, y, rd_seed

if __name__ == '__main__':
  main()
