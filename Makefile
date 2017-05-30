lambdas := Authorize AuthorizeToken DeleteSnippetFromS3 GetSnippetFromS3 GetIndexes SaveSnippetToS3 GenerateIndexFiles GitHubAccessCodeGetter UpdateSnippetInS3 ReparseSnippets #CleanUp
zipdir := zips
lambdadir := lambdas
.PHONY = all clean test test-api $(lambdas)

all: $(lambdas)

#Set package variables for lambdas that need them
Authorize: packages = requests
AuthorizeToken: packages = requests
GitHubAccessCodeGetter: packages = requests
CleanUp: packages = requests

#Set parser variables for packages that need them
ReparseSnippets: parsers = java8.min.js python3.min.js

#Nice alias so only the lambda name need be invoked
$(lambdas): % : $(zipdir) $(zipdir)/%.zip
$(zipdir):
	mkdir -p $@
$(zipdir)/%.zip:
	mkdir -p tmp
	if [ -e $(lambdadir)/$*/lambda_function.py ]; then \
		cp $(lambdadir)/$*/lambda_function.py tmp && \
		pip install -t tmp $(packages); \
	else \
		cp $(lambdadir)/$*/* tmp; \
	fi
	cd tmp && zip -r $* .
	mv tmp/$*.zip $(zipdir)
	rm -rf tmp

clean:
	rm -rf $(zipdir)
test:
	python -m unittest discover -v -s __tests__
test-api:
	bash api_tests/run-tests
