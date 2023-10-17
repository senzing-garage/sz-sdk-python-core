
# echo "C:\Program Files\Senzing\g2\lib" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append
echo "C:\PROGRA~1\Senzing\g2\lib" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append
$Env:Path
$Env:PATH += ";$pwd"
$Env:Path
python3 -m unittest tests/g2config_test.py tests/g2configmgr_test.py tests/g2diagnostic_test.py tests/g2engine_test.py tests/g2engineflags_test.py tests/g2exception_test.py tests/g2hasher_test.py tests/g2product_test.py
