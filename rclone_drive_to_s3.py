import rclone

cfg_path = r'/Users/noelnathanieljimenofonseca/.config/rclone/rclone.conf'

with open(cfg_path) as f:
   cfg = f.read()

result = rclone.with_config(cfg).listremotes()

#print(result)

rclone.with_config(cfg).run_cmd(command='sync', extra_args=["-v", "--ignore-checksum", "mygoogledrive1:/", "mys3_1:/noelbeerbucket"])

# print(rclone.with_config(cfg).run_cmd(command='ls', extra_args=["-v", "mys3_1:/noelbeerbucket"]))