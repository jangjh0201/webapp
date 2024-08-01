import secrets

# secret_key 생성
secret_key = secrets.token_hex(32)
print(secret_key)
# # .env 파일 경로
# env_file_path = '.env'

# # .env 파일 내용을 읽어와서 업데이트 또는 추가
# with open(env_file_path, 'r') as f:
#     lines = f.readlines()

# with open(env_file_path, 'w') as f:
#     found_secret_key = False
#     for line in lines:
#         if line.startswith('SECRET_KEY='):
#             f.write(f'SECRET_KEY={secret_key}\n')
#             found_secret_key = True
#         else:
#             f.write(line)
#     if not found_secret_key:
#         f.write(f'SECRET_KEY={secret_key}\n')

# print(f'SECRET_KEY={secret_key}')
