

python3

d = {
	"abc" : "abcdefg!",                   #test scalar first
	"li"  : [1, 2, {"bucklemy": "shoe"}], #test list, dict-in-list
}

from trix.x.nav import * 
n = Nav(d)
g = iter(n.navgen())

x = next(g)
x.path()




# hold on to this
x = xnaviter(iter(n))



