// from: http://www.daveamenta.com/2011-05/programmatically-or-command-line-change-the-default-sound-playback-device-in-windows-7/

#define EXTERN_DLL_EXPORT extern "C" __declspec(dllexport)

#include <vector>
#include <iostream>
#include <atlstr.h>
#include <atlsafe.h>
#include "windows.h"
#include "Propidl.h"
#include "Mmdeviceapi.h"
#include "PolicyConfig.h"
#include "Functiondiscoverykeys_devpkey.h"
using namespace std;

const int GET_DEVICES = 0;
const int SET_DEFAULT_DEVICE = 1;


HRESULT SetDefaultAudioPlaybackDevice(LPCWSTR devID)
{
    IPolicyConfigVista *pPolicyConfig;
    ERole reserved = eConsole;

    HRESULT hr = CoCreateInstance(__uuidof(CPolicyConfigVistaClient),
        NULL, CLSCTX_ALL, __uuidof(IPolicyConfigVista), (LPVOID *)&pPolicyConfig);
    if (SUCCEEDED(hr))
    {
        hr = pPolicyConfig->SetDefaultEndpoint(devID, reserved);
        pPolicyConfig->Release();
    }
    return hr;
}

// EndPointController.exe [NewDefaultDeviceID]
int work(int argc, int code, vector<wstring>& deviceStrArr = vector<wstring>())
{
    // read the command line option, -1 indicates list devices.
    int option = -1;
    if (argc == SET_DEFAULT_DEVICE)
    {
        option = code;
    }

    HRESULT hr = CoInitialize(NULL);
    if (SUCCEEDED(hr))
    {
        IMMDeviceEnumerator *pEnum = NULL;
        // Create a multimedia device enumerator.
        hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL,
            CLSCTX_ALL, __uuidof(IMMDeviceEnumerator), (void**)&pEnum);
        if (SUCCEEDED(hr))
        {
            IMMDeviceCollection *pDevices;
            // Enumerate the output devices.
            hr = pEnum->EnumAudioEndpoints(eRender, DEVICE_STATE_ACTIVE, &pDevices);
            if (SUCCEEDED(hr))
            {
                UINT count;
                pDevices->GetCount(&count);
                if (SUCCEEDED(hr))
                {
                    for (UINT i = 0; i < count; i++)
                    {
                        IMMDevice *pDevice;
                        hr = pDevices->Item(i, &pDevice);
                        if (SUCCEEDED(hr))
                        {
                            LPWSTR wstrID = NULL;
                            hr = pDevice->GetId(&wstrID);
                            if (SUCCEEDED(hr))
                            {
                                IPropertyStore *pStore;
                                hr = pDevice->OpenPropertyStore(STGM_READ, &pStore);
                                if (SUCCEEDED(hr))
                                {
                                    PROPVARIANT friendlyName;
                                    PropVariantInit(&friendlyName);
                                    hr = pStore->GetValue(PKEY_Device_FriendlyName, &friendlyName);
                                    if (SUCCEEDED(hr))
                                    {
                                        // if no options, print the device
                                        // otherwise, find the selected device and set it to be default
                                        if (option == -1)
                                        {
                                            wstring str = wstring(friendlyName.pwszVal);
                                            deviceStrArr.push_back(str);
                                        }
                                        if (i == option) SetDefaultAudioPlaybackDevice(wstrID);
                                        PropVariantClear(&friendlyName);
                                    }
                                    pStore->Release();
                                }
                            }
                            pDevice->Release();
                        }
                    }
                }
                pDevices->Release();
            }
            pEnum->Release();
        }
    }
    return hr;
}

EXTERN_DLL_EXPORT const wchar_t* StrSoundDevices() {
    vector<wstring> devicesStrArr;
    HRESULT result = work(GET_DEVICES, NULL, devicesStrArr);
    wstring s;
    for (size_t i = 0; i < devicesStrArr.size(); i++) {
        wstring str = devicesStrArr[i];
        s += wstring(str + L"\1");
    }
    size_t size = s.size() + 1;
    wchar_t* str = (wchar_t*)CoTaskMemAlloc(size * sizeof(wchar_t));
    wcscpy_s(str, size, s.c_str());
    return str;
}

EXTERN_DLL_EXPORT HRESULT SetDefaultSoundDevice(int code) {
    return work(SET_DEFAULT_DEVICE, code);
}