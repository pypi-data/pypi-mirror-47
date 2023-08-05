# oracle

需要python3.6的环境

## 安装virtualenv
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt

$ npm install -g crypto-tx
$ crypto-tx -h
Usage:
  crypto-tx -G [-json]
  crypto-tx -E [-k privateKey] -p publicKeyTo -d originaltext [-iv value] [-json]
  crypto-tx -D -k privateKey -p ephemPublicKey -d ciphertext -iv value
Options:
  -E   cmd encryptECIES [no]
  -D   cmd decryptECIES [no]
  -G   cmd gen private and public keys [no]
  -k   privateKey hex
  -p   publicKey hex
  -d   encrypt or decrypt data
  -iv  IV 16 bytes hex
  -json convert json [no]
 
 ```
 
 # 生成golang的so文件
 ```bash
 $ cd $PAHT/golang
 $ make
 ```
 