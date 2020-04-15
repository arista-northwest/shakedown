

from asyncio.tasks import wait_for
import pytest
import time
import sys
import pexpect

from shakedown import ssh

@pytest.fixture(scope="session")
def get_version_ssh():
    def _get_version_ssh(dut):
        session = ssh.Session()
        session.open(dut.host, auth=dut.auth)
        return session.send("show version")
    return _get_version_ssh

@pytest.fixture(scope="session")
def reload():
    def _reload(dut, save: bool = False, waitfor: int = 300):
        session = ssh.Session()
        session.open(dut.host, auth=dut.auth)
        if save:
            session.send('write')

        try:
            session.send('reload now')
            while session.alive:
                pass
        except ssh.SshSessionClosedException:
            pass
        except pexpect.EOF:
            pass

        time.sleep(30)
        
        session.close()

        if waitfor > 0:
            t0 = time.time()
            while True:
                try:
                    session.reopen()
                    while True:
                        line = "show logging last 30 seconds | i SYSTEM_RESTARTED'"
                        output = session.send(line)

                        if "System restarted" in output:
                            sys.stdout.write("!\n")
                            sys.stdout.flush()
                            return

                        sys.stdout.write("?")
                        sys.stdout.flush()

                        if int(time.time() - t0) >= waitfor:
                            raise ValueError("Timeout exceeded")

                        time.sleep(5)

                except pexpect.EOF:
                    pass
                except pexpect.TIMEOUT:
                    pass
                except ssh.SshSessionClosedException:
                    pass

                sys.stdout.write(".")
                sys.stdout.flush()

                if int(time.time() - t0) >= waitfor:
                    raise ValueError("Timeout exceeded")

            time.sleep(10)
    
    return _reload