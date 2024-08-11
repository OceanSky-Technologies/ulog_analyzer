import os


def get_multi_id_num(tmp_dirname: str, message_name: str):
    files = [
        name for name in os.listdir(tmp_dirname) if os.path.isfile(tmp_dirname + "/" + name) and message_name in name
    ]

    return len(files)


def get_csv_file(tmp_dirname: str, ulog_filename: str, message_name: str, multi_id: 0):
    output_file_prefix = ulog_filename

    # strip '.ulg'
    if output_file_prefix.lower().endswith(".ulg"):
        output_file_prefix = output_file_prefix[:-4]

    base_name = os.path.basename(output_file_prefix)
    output_file_prefix = os.path.join(tmp_dirname, base_name)

    fmt = "{0}_{1}_{2}.csv"
    return fmt.format(output_file_prefix, message_name, str(multi_id))
