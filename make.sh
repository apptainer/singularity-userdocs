for i in admin-guide user-guide;do
	if [ -r "$i.tex" ]; then
		docker run -v `pwd`:/source jagregory/pandoc  -f latex --toc --toc-depth=2  $i.tex -o $i.rst
	fi
done
