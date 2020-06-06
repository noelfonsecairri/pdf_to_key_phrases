import rclone

cfg_path = r'/Users/noelnathanieljimenofonseca/.config/rclone/rclone.conf'

with open(cfg_path) as f:
   cfg = f.read()

result = rclone.with_config(cfg).listremotes()

#print(result)

#COPY Google drive to S3
rclone.with_config(cfg).run_cmd(command='copy', extra_args=["-v", "--ignore-checksum", "mygoogledrive1:/", "mys3_1:/noelbeerbucket"])

#SYNC Google drive to S3
# rclone.with_config(cfg).run_cmd(command='sync', extra_args=["-v", "--ignore-checksum", "mygoogledrive1:/", "mys3_1:/noelbeerbucket"])

# S3 to Google Drive
# rclone.with_config(cfg).run_cmd(command='sync', extra_args=["-v", "--ignore-checksum", "mys3_1:/noelbeerbucket", "mygoogledrive1:/"])

# print(rclone.with_config(cfg).run_cmd(command='ls', extra_args=["-v", "mys3_1:/noelbeerbucket"]))