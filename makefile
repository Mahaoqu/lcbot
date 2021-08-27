include .env

PACKAGE_NAME=slack-lcbot-package.zip 
FUNCTION_NAME=slack-lcbot
GREETING_NAME=lc-morning-greeting

all: slack-lcbot lc-morning-greeting

slack-lcbot-package.zip: *.py
	pip install --target ./build --no-deps -r requirements.txt
	cd build; zip -r ../${PACKAGE_NAME} .
	zip -g ${PACKAGE_NAME} *.py pb.csv

slack-lcbot: slack-lcbot-package.zip .env
	aws lambda update-function-code --function-name $@ \
		--zip-file fileb://${PACKAGE_NAME} --no-cli-pager
	aws lambda update-function-configuration --function-name $@ \
    	--environment "Variables={SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}}" \
		--handler app.handler --no-cli-pager

lc-morning-greeting: slack-lcbot-package.zip .env
	aws lambda update-function-code --function-name $@ \
		--zip-file fileb://${PACKAGE_NAME} --no-cli-pager
	aws lambda update-function-configuration --function-name $@ \
    	--environment "Variables={SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET},LC_CHANNEL_ID=${LC_CHANNEL_ID}}" \
		--handler morning.greeting --no-cli-pager

clean:
	-rm -rf build/
	-rm ${PACKAGE_NAME}
