# Execute os testes usando pytest
pytest tests/

# Verifique o código de saída dos testes
pytest_exit_code=$?

if [ $pytest_exit_code -ne 0 ]; then
  # Tests failed, so exit with a non-zero status
  echo "Tests Failed. Application will not be started."
  exit 1
fi

echo "Test Passed!!!"
echo "Starting Application"
python3 ./src/main.py

# Verifique o código de saída da aplicação Python
python_exit_code=$?

if [ $python_exit_code -ne 0 ]; then
  # Application failed, so exit with a non-zero status
  echo "Application failed."
  exit 1
fi

echo "Application Finished"
exit

while true; do
  sleep 1
done
