#!/bin/bash
if [[ $1 == 'dev' ]]
then
	COMMIT=$([ "$2" == '' ] && echo "Dev" || echo "$2")
	git add .
	git commit -m "$COMMIT"
	git pull
	git push
	gcloud compute scp --recurse ./ backend-01:./learning-dev
else
	COMMIT=$([ "$1" == '' ] && echo "Update" || echo "$1")
	git add .
	git commit -m "$COMMIT"
	git pull
	git push
	gcloud compute scp --recurse ./ backend-01:./learning
fi
