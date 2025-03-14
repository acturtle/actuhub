import pandas as pd
from io import StringIO


def exec_command(ssh, command, show_output=False):
    try:
        # Get the output and errors
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout_content = stdout.read().decode("utf-8")
        stderr_content = stderr.read().decode("utf-8")

        if show_output:
            if stdout_content:
                print(f"Stdout:\n{stdout_content}")
            if stderr_content:
                print(f"Stderr:\n{stderr_content}")

    except Exception as e:
        print(f"Exception:\n{str(e)}")

    return None


def load_from_s3(s3_client, bucket_name, key, index_col=None):
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    csv_content = response["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_content))
    if index_col and index_col in df.columns:
        df.set_index(index_col, inplace=True)
    return df


def aggregate(output_chunk1, output_chunk2, diagnostic):
    # Prepare the result DataFrame
    result = pd.DataFrame()

    # Iterate over the diagnostic DataFrame
    for _, row in diagnostic.iterrows():
        column = row['variable']
        agg_type = row['aggregation_type']

        if agg_type == 'sum':
            result[column] = output_chunk1[column] + output_chunk2[column]
        elif agg_type == 'first':
            result[column] = output_chunk1[column]
        else:
            raise ValueError(f"Unknown aggregation type: {agg_type}")

    # Add time
    result.insert(0, 't', output_chunk1['t'])

    return result
