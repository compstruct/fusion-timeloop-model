import argparse
'''
FILE_START = "../../CIFAR10-Fusion/"

for i in range(1,16):
    if i != 12:
        f = open("{}b{}/org/comp/prob/prob.yaml".format(FILE_START, i))

        C = 0
        M = 0
        R = 0
        S = 0
        for l in f.readlines():
            if l.find("C:") >= 0:
                C = int(l.split(": ")[1].strip())
            elif l.find("M:") >= 0:
                M = int(l.split(": ")[1].strip())
            elif l.find("R:") >= 0:
                R = int(l.split(": ")[1].strip())
            elif l.find("S:") >= 0:
                S = int(l.split(": ")[1].strip())
        print("({},{},{},{})".format(R,S,C,M))
'''
parser = argparse.ArgumentParser()
parser.add_argument("--comp", type=int)
args = parser.parse_args()
print(args.comp)


if args.comp == 1:
    func_name = "comp"
elif args.comp == 0:
    func_name = "decomp"
else:
    func_name = "conv"

print("def {}_worktiles(tensor, b):".format(func_name))
for i in range(1,17):
    #if i != 12:
    print("\t{}if b == {}:".format("el" if i > 1 else "", i))
    print("\t\tprint('Running {}{}()')".format(func_name, i))
    print("\t\treturn {}{}(tensor)".format(func_name, i))
