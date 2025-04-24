@echo off
setlocal
echo :arrows_counterclockwise: Cleaning previous build...
cd src\simplifyapp\resources
rmdir /s /q build
mkdir build
cd build
echo :wrench: Configuring build with CMake...
cmake .. -DCMAKE_BUILD_TYPE=Release ^
         -DCMAKE_TOOLCHAIN_FILE=C:/Users/JAMBROCIOALCANTARA/vcpkg/scripts/buildsystems/vcpkg.cmake ^
         -DVCPKG_TARGET_TRIPLET=x64-windows-static
echo :hammer: Building mesh_wrapper...
cmake --build . --config Release
echo :truck: Copying binary to ..\bin\
mkdir ..\bin 2>nul
copy Release\mesh_wrapper.exe ..\bin\
echo :white_check_mark: Done! Binary is at src\simplifyapp\resources\bin\mesh_wrapper.exe
endlocal