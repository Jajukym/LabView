/*example code for LabView with function name "int_Multiply(int32, int32)"*/
#include "pch.h"

extern "C" __declspec(dllexport) int __cdecl Multiply(int a, int b);	/*add function name to this line*/

BOOL APIENTRY DllMain( HMODULE hModule,									/*generates the .dll, note Release and x64 options*/
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

__declspec(dllexport) int __cdecl Multiply(int a, int b)				/*add function name to this line*/
{
	return a * b;
}

/**********************************/
/*          On LabView            */
/**********************************/
/*Use "Call Library Function Node"*/
/*Input path to .dll              */
/*Input function name             */
/*Input parameters called out     */
/*Click OK                        */
/**********************************/