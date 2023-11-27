from cx_Freeze import setup, Executable

setup(
    name="CustomReport",
    version="1.0",
    description="Custom Report for sonarqube",
    executables=[Executable("run.py")],
)
