lambdas := Authorize AuthorizeToken DeleteSnippetFromS3 GetSnippetFromS3 SaveSnippetToS3 GenerateIndexFiles GitHubAccessCodeGetter UpdateSnippetInS3
zipdir := zips
lambdadir := lambdas
scriptsdir := scripts
.PHONY = all clean publish test $(lambdas)

all: $(lambdas)

#Set package variables for lambdas that need them
Authorize: packages = axios
AuthorizeToken: packages = axios
GithubAccessCodeGetter: packages = axios lodash
SaveSnippetToS3: scripts = schema
SaveSnippetToS3: packages = cerberus
UpdateSnippetInS3: scripts = schema
UpdateSnippetInS3: packages = cerberus


#Nice alias so only the lambda name need be invoked
$(lambdas): % : $(zipdir) $(zipdir)/%.zip
$(zipdir):
	mkdir -p $@
$(zipdir)/%.zip:
	mkdir -p tmp
	if [ -e $(lambdadir)/$*/index.js ]; then \
		cp $(lambdadir)/$*/index.js tmp && \
		npm install --prefix=tmp $(packages); \
	else \
		cp $(lambdadir)/$*/lambda_function.py tmp && \
		pip install -t tmp $(packages); \
	fi
	for script in $(scripts); do \
		cp $(scriptsdir)/$$script.py tmp; \
	done
	cd tmp && zip -r $* .
	mv tmp/$*.zip $(zipdir)
	rm -rf tmp

clean:
	rm -rf $(zipdir)

test:
	python -m unittest discover -t . -s __tests__
