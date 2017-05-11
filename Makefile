lambdas := Authorize AuthorizeToken DeleteSnippetFromS3 GetSnippetFromS3 GetIndexes SaveSnippetToS3 GenerateIndexFiles GitHubAccessCodeGetter UpdateSnippetInS3
zipdir := zips
lambdadir := lambdas
.PHONY = all clean test test-api $(lambdas)

all: $(lambdas)

#Set package variables for lambdas that need them
Authorize: packages = requests
AuthorizeToken: packages = requests
GitHubAccessCodeGetter: packages = requests


#Nice alias so only the lambda name need be invoked
$(lambdas): % : $(zipdir) $(zipdir)/%.zip
$(zipdir):
	mkdir -p $@
$(zipdir)/%.zip:
	mkdir -p tmp
	cp $(lambdadir)/$*/lambda_function.py tmp && \
	pip install -t tmp $(packages)
	cd tmp && zip -r $* .
	mv tmp/$*.zip $(zipdir)
	rm -rf tmp

clean:
	rm -rf $(zipdir)
test:
	python -m unittest discover -v -s __tests__
test-api:
	bash api_tests/run-tests
