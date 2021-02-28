build-reveal:
	cd reveal.js
	npm install
	cd ..
	
theme:
	cd reveal.js; npm run build -- css-themes
	mkdir -p slides/reveal.js
	cp -R reveal.js/dist slides/reveal.js
	
slides: 
	python make_slides.py
	
serve:
	python make_slides.py --serve True --watch True