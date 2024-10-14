import time

import pytest

from common.all_paths import ACBN_ADD_UPLOAD
from testcase_py.upload_network_files import upload_files

if __name__ == '__main__':
    for i in range(0, 3):
        print(f"执行第 {i} 次")
        upload_files()
        time.sleep(2)
        pytest.main(['-sv', ACBN_ADD_UPLOAD])