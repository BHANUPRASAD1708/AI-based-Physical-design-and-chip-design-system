import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stable_baselines3 import PPO
from environment import DynamicChipEnv
from heapq import heappush, heappop
import numpy as np

env = DynamicChipEnv()
model = PPO.load("chip_designer")

obs,_=env.reset()
done=False
while not done:
    action,_=model.predict(obs)
    obs,_,done,_,_=env.step(action)

grid=np.zeros((env.width,env.height))
pins={}

for block,(x,y) in env.layout.items():
    w,h=env.blocks[block]
    grid[x:x+w,y:y+h]=1
    pin_x=x+w//2
    pin_y=y+h
    if pin_y>=env.height:
        pin_y=y-1
    pins[block]=(pin_x,pin_y)

def astar(start,goal):
    open=[]
    heappush(open,(0,start))
    came={}
    g={start:0}

    while open:
        _,cur=heappop(open)
        if cur==goal:
            path=[]
            while cur in came:
                path.append(cur)
                cur=came[cur]
            path.append(start)
            return path[::-1]

        x,y=cur
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<env.width and 0<=ny<env.height:
                if grid[nx][ny]==1 and (nx,ny)!=goal:
                    continue
                new=g[cur]+1
                if (nx,ny) not in g or new<g[(nx,ny)]:
                    came[(nx,ny)]=cur
                    g[(nx,ny)]=new
                    f=new+abs(nx-goal[0])+abs(ny-goal[1])
                    heappush(open,(f,(nx,ny)))
    return []

fig=plt.figure(figsize=(9,7))
ax=fig.add_subplot(111,projection='3d')

# Draw blocks
for block,(x,y) in env.layout.items():
    w,h=env.blocks[block]
    ax.bar3d(y,x,0,h,w,3,color="gold",edgecolor="black")
    ax.text(y+h/2,x+w/2,3.2,block,ha="center",fontsize=8)

# ------------------------------------------------
# INNOVUS STYLE CHANNEL ROUTING (ONLY CHANGE)
# ------------------------------------------------
colors=["#1976d2","#388e3c","#7b1fa2",
        "#f57c00","#c2185b"]

track_spacing = 2
track_base = 1
metal_z = 0.5   # routing layer close to floor

for i,(b1,b2) in enumerate(env.connections):

    if b1 in pins and b2 in pins:

        x1,y1 = pins[b1]
        x2,y2 = pins[b2]

        # choose routing channel
        channel = track_base + i*track_spacing
        if channel >= env.height:
            channel = env.height - 2

        color = colors[i % len(colors)]

        # horizontal from source
        ax.plot(
            [y1,channel],
            [x1,x1],
            [metal_z,metal_z],
            color=color,lw=2
        )

        # vertical channel routing
        ax.plot(
            [channel,channel],
            [x1,x2],
            [metal_z,metal_z],
            color=color,lw=2
        )

        # horizontal to destination
        ax.plot(
            [channel,y2],
            [x2,x2],
            [metal_z,metal_z],
            color=color,lw=2
        )

ax.set_xlim(0,env.width)
ax.set_ylim(0,env.height)
ax.set_zlim(0,7)
ax.set_box_aspect([env.width,env.height,7])

plt.title("Correct Physical 3D Metal Routing")
plt.show()