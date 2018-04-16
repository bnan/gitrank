import requests
import itertools
from pprint import pprint
a = [
	["numpy/numpy", "pandas-dev/pandas"],
	["scipy/scipy", "pandas-dev/pandas"],
	["numpy/numpy", "scipy/scipy"],

	["matplotlib/matplotlib", "mwaskom/seaborn"],
	["yhat/ggpy", "mwaskom/seaborn"],
	["matplotlib/matplotlib", "yhat/ggpy"],
	["matplotlib/matplotlib", "Kozea/pygal"],
	["Kozea/pygal", "mwaskom/seaborn"],
	["Kozea/pygal", "yhat/ggpy"],

]

a.extend([list(x) for x in itertools.combinations([
		"funny-falcon/auto_numeric_js",
		"josdejong/lossless-json",
		"stdlib-js/stdlib",
		"dyoo/js-numbers",
		"kevinongko/vue-numeric"],
		2)])


a.extend([list(x) for x in itertools.combinations([
		"Idnan/bash-guide",
		"alexanderepstein/Bash-Snippets",
		"mydzor/bash2048",
		"magicmonty/bash-git-prompt",
		],2)])

a.extend([list(x) for x in itertools.combinations([
		"AnyChart/GraphicsJS",
		"luileito/jsketch",
		"anvaka/VivaGraphJS",
		"koggdal/ocanvas",
		"tristen/pencil"
		],2)])

a.extend([list(x) for x in itertools.combinations([
		"sobolevn/awesome-cryptography",
		"pyca/cryptography",
		"jedisct1/libsodium",
		"google/tink",
		"jedisct1/libhydrogen"
		],2)])


pprint(a)

a = [[x[0].replace("/", "."), x[1].replace("/", ".")] for x in a]

for pair in a:
	print(pair)
	requests.get('http://0.0.0.0:1337/api/v1/repository/' + pair[0] + '/' + pair[1] + '/')
