lambdas := Authorize AuthorizeToken DeleteSnippetFromS3 GetSnippetFromS3 GetIndexes SaveSnippetToS3 GenerateIndexFiles GitHubAccessCodeGetter UpdateSnippetInS3
zipdir := zips
lambdadir := lambdas
.PHONY = all clean publish $(lambdas)

all: $(lambdas)

#Set package variables for lambdas that need them
Authorize: packages = requests
AuthorizeToken: packages = requests
GitHubAccessCodeGetter: packages = requests
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
	cd tmp && zip -r $* .
	mv tmp/$*.zip $(zipdir)
	rm -rf tmp

clean:
	rm -rf $(zipdir)
