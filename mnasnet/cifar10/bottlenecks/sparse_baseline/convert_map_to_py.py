import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)
parser.add_argument("--name", type=str)
args = parser.parse_args()


FILE_NAME=args.file

f = open(FILE_NAME)

# moved to bash script
#print("import numpy as np\n")
print("def {}(tensor):".format(args.name))
print("\tworktiles = {}")

tier = 1
spatial_tier = 0

axis_lookup = {}
comment = ""

spatial_lookup = {}

for l in f.readlines():
    if l.find("for") >= 0:
        axis = l.split("for")[1].split("in")[0].strip()
        upper_bound = int(l.split(":")[1].split(")")[0])
        if axis in axis_lookup.keys():
            axis_lookup[axis].append(upper_bound)
        else:
            axis_lookup[axis] = [upper_bound]
        tabs = "\t"*tier

        if l.find("Spatial") >= 0:
            comment = "# {}".format(l.split(" ")[-1].strip())
            spatial_axis = l.split(" ")[-1].split("-")[1].split(")")[0]

            if spatial_axis in spatial_lookup.keys():
                spatial_lookup[spatial_axis].append(("{}{}".format(axis, len(axis_lookup[axis]) - 1), upper_bound))
            else:
                spatial_lookup[spatial_axis] = [("{}{}".format(axis, len(axis_lookup[axis]) - 1), upper_bound)]

        else:
            comment = ""

        print("{}for {}{} in range({}): {}".format(tabs, axis, len(axis_lookup[axis]) - 1, upper_bound, comment))
        tier += 1
    elif l.find("[") >= 0:
        if l.find("ifmap") >= 0:
            # do other stuff
            x_str = "x ="
            x_vars = spatial_lookup["X"]
            x_vars.reverse()
            prod = 1

            for i, t in enumerate(x_vars):
                adjusted_i = len(x_vars) - i - 1
                x_str += " {}*{}".format(t[0], prod)
                prod *= t[1]
                if adjusted_i > 0:
                    x_str += " +"
            y_str = "y ="
            y_vars = spatial_lookup["Y"]
            y_vars.reverse()
            prod = 1

            for i, t in enumerate(y_vars):
                adjusted_i = len(y_vars) - i - 1
                y_str += " {}*{}".format(t[0], prod)
                prod *= t[1]
                if adjusted_i > 0:
                    y_str += " +"
            print("{}{}".format("\t"*tier, x_str))
            print("{}{}".format("\t"*tier, y_str))
            print("{}worktile = []".format("\t"*tier))
            spatial_tier = tier
        print("{}# {}".format("\t"*tier, l.split(" ")[0]))

for k, v in axis_lookup.items():
    var = "{} =".format(k)
    v.reverse()
    prod = 1
    for i, t in enumerate(v):
        adjusted_i = len(v) - i - 1
        var += " {}{}*{}".format(k, adjusted_i, prod)
        prod *= t
        if adjusted_i > 0:
            var += " +"
    print("{}{}".format(tier*"\t", var))

if "R" not in axis_lookup.keys():
    print("{}R = 0".format("\t"*tier))
    print("{}S = 0".format("\t"*tier))

if 'conv' in FILE_NAME:
    print("{}worktile.append(tensor[R,S,M])".format("\t"*tier))
else:
    print("{}worktile.append(tensor[R,S,C,M])".format("\t"*tier))

print("{}if (x,y) in worktiles.keys():".format("\t"*spatial_tier))
print("{}worktiles[(x,y)].append(np.array(worktile))".format("\t"*(spatial_tier + 1)))
print("{}else:".format("\t"*spatial_tier))
print("{}worktiles[(x,y)] = [np.array(worktile)]".format("\t"*(spatial_tier + 1)))
print("\treturn worktiles")
