import "libraries/IndexLib.sol";
import "libraries/ColumnLib.sol";


/// @title RowLib - ????
/// @author PiperMerriam - <pipermerriam@gmail.com>
library RowLib {
        /*
         *  TODO
         *
         *  Address: TODO
         */
        struct Table {
                ColumnLib[] columns;
                bool indexed;
                IndexLib.Index index;
        }
}

