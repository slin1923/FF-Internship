from cleaner import Cleaner

def test_read_file():
    """
    simple sanity test on sample dataset from my first Nikon data extraction recipe
    """
    clnr = Cleaner("9574A1_Golden_Wafer_Nikon_out_2.1.csv")
    nom_X, nom_Y, meas_X, meas_Y = clnr.extract_XY()
    meas_X_widths, meas_Y_widths = clnr.extract_widths()
    print(nom_X, nom_Y, meas_X, meas_Y)
    print(meas_X_widths, meas_Y_widths)

if __name__ == '__main__':
    test_read_file()