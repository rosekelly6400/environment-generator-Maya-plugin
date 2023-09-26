#include <maya/MIOStream.h>
#include <maya/MSimple.h>
#include <maya/MDoubleArray.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"


// Use a Maya macro to setup a simple interpretMap class
// with methods for initialization, etc.
//
DeclareSimpleCommand( interpretMap, PLUGIN_COMPANY, "4.5");

// takes in filename and iterates through the file data to
// create and return array of RGB values
//
MStatus interpretMap::doIt( const MArgList& args )
{
    cout << "interpretMap executing "  << endl;
    std::string filename = args.asString(0).asChar();

    // ... x = width, y = height, n = # 8-bit components per pixel ...

    MDoubleArray result;

    unsigned char* data = stbi_load(filename.c_str(), &x, &y, &n, 0);

    cout << "parse file " << endl;

    result.append(x);
    result.append(y);
    result.append(n);

    int totalValues = x * y * n;

    // process data if not NULL
    if (data != nullptr && x > 0 && y > 0)
    {
        cout << "non-null File " << endl;
        if (n == 3)
        {
            int size = strlen((char*)data);
           cout << "OG FILE First pixel: RGB "
                << static_cast<int>(data[0]) << " "
                << static_cast<int>(data[1]) << " "
                << static_cast<int>(data[2]) << '\n';
           int x = 0;
           int y = 0;
           for (int i = 0; i < totalValues; i += 3) {
               if (x == 6)
               {
                   cout << '\n';
                   y++;
                   x = 0;
               }
               cout << "Pixel " << "(" << x << ", " << y << ") " << ": RGB "
                   << static_cast<int>(data[0 + i]) << " "
                   << static_cast<int>(data[1 + i]) << " "
                   << static_cast<int>(data[2 + i]) << '\t';

               result.append(static_cast<int>(data[0 + i]));
               result.append(static_cast<int>(data[1 + i]));
               result.append(static_cast<int>(data[2 + i]));

               x++;
           }
        }
        else if (n == 4)
        {
            int size = strlen((char*)data);
            cout << data << '\n';
            cout << "First pixel: RGBA "
                << static_cast<int>(data[0]) << " "
                << static_cast<int>(data[1]) << " "
                << static_cast<int>(data[2]) << " "
                << static_cast<int>(data[3]) << '\n';
            int x = 0;
            int y = 0;
            for (int i = 0; i < totalValues; i += 4) {
                if (x == 6)
                {
                    cout << '\n';
                    y++;
                    x = 0;
                }
                cout << "Pixel " << "(" << x << ", " << y << ") " << ": RGBA "
                          << static_cast<int>(data[0+i]) << " "
                          << static_cast<int>(data[1+i]) << " "
                          << static_cast<int>(data[2+i]) << " "
                          << static_cast<int>(data[3+i]) << '\t';
                result.append(static_cast<int>(data[0 + i]));
                result.append(static_cast<int>(data[1 + i]));
                result.append(static_cast<int>(data[2 + i]));
                result.append(static_cast<int>(data[3 + i]));

                x++;
            }
        }
        clearResult();
        setResult(result);
    }
    else
    {
        cout << "Error\n";
    }
	return MS::kSuccess;
}
