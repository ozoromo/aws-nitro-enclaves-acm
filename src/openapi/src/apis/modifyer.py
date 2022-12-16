from os.path import exists

if not exists("default_api.rs.bak"):
    print("No backup found!")
    print("Backing up default_api.rs")



input_file = open("default_api.rs.bak", "r")
input_lines = input_file.readlines()
input_file.close()

output_file = open("default_api.rs", "w")

output_lines = []
bracket_count = 0

in_function = False
started = False

for line in input_lines:
    if "pub fn config_backup_passphrase_put(" in line:
        started = True

    if not started:
        output_lines.append(line)
        continue
    if "{" in line:
        bracket_count += 1


    if "}" in line:
        bracket_count -= 1


    if line.startswith("pub fn health_ready_get"):
        output_lines.append(line)
        continue

    if "-> Result<" in line and "Error<HealthReadyGetError>>" not in line:
            output_lines.append(line)
            output_lines.append("unimplemented!();")
            output_lines.append("/*")
            continue

    if "}" in line and bracket_count == 0:
        output_lines.append("*/")
        output_lines.append("}")
        continue

    output_lines.append(line)

output_file.writelines(output_lines)

