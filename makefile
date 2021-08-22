include .env

PACKAGE_NAME=slack-lcbot-package.zip 
FUNCTION_NAME=slack-lcbot

deploy: 
	pip install --target ./build -r requirements.txt
	cd build; zip -r ../${PACKAGE_NAME} .
	zip -g ${PACKAGE_NAME} *.py
	aws lambda update-function-code --function-name ${FUNCTION_NAME} \
		--zip-file fileb://${PACKAGE_NAME} --no-cli-pager
	aws lambda update-function-configuration --function-name ${FUNCTION_NAME} \
    	--environment "Variables={SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}}" \
		--handler app.handler --no-cli-pager
clean:
	-rm -rf build/
	-rm ${PACKAGE_NAME}
