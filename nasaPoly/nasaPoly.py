import re
import math
from pathlib import Path
'''Example data:

H2O               CODATA 1989. JRNBS 1987 v92 p35. TRC tuv-25 10/88.
 2 g 8/89 H   2.00O   1.00    0.00    0.00    0.00 0   18.0152800    -241826.000
    200.000  1000.000 7 -2.0 -1.0  0.0  1.0  2.0  3.0  4.0  0.0         9904.092
-3.947960830D+04 5.755731020D+02 9.317826530D-01 7.222712860D-03-7.342557370D-06
 4.955043490D-09-1.336933246D-12 0.000000000D+00-3.303974310D+04 1.724205775D+01
   1000.000  6000.000 7 -2.0 -1.0  0.0  1.0  2.0  3.0  4.0  0.0         9904.092
 1.034972096D+06-2.412698562D+03 4.646110780D+00 2.291998307D-03-6.836830480D-07
 9.426468930D-11-4.822380530D-15 0.000000000D+00-1.384286509D+04-7.978148510D+00
'''

raw_data_path = Path(__file__).parent / 'raw.dat'

print_str = '''
Species Name: {}
Data Source: {}
Molecular wt: {} g/mol
Valid temperature range(s): {}
'''

def _getEntry(name):
    with open(raw_data_path, 'r') as raw_data_file:
        raw_data = raw_data_file.read()
        entry = [s.strip() for s in re.split('\n(?=[a-zA-Z])', raw_data) if s[0:16].strip() == name]
        return(entry)

class Species():
    def __init__(self, name):
        self.R = 8.3145 # J/mol-K
        self.species_name = name
        self.raw_entry = _getEntry(name)
        if len(self.raw_entry) == 0:
            print('"{} was not found in the database!"'.format(name))
            raise ValueError
        elif len(self.raw_entry) > 1:
            print('Found multiple entries for "{}". Something is wrong!'.format(name))
            raise ValueError
        lines = self.raw_entry[0].split('\n')
        self.source = lines[0][18:80].strip()
        self.num_T_ints = int(lines[1][0:2])
        self.ref_data_code = lines[1][3:9]
        self.chem_formula = lines[1][10:50]
        self.phase = int(lines[1][50:52])
        self.phase_name = {0: 'gas', 1: 'solid', 2: 'liquid'}[self.phase]
        self.moleculr_wt = float(lines[1][52:65])
        self.h_f_0 = float(lines[1][65:80]) # heat of formation at 298.15 K, J/mol
        if self.num_T_ints > 0:
            self.delta_h_0 = float(lines[2][65:80]) # h_0(298.15)–h_0(0) J/mol, if available 
        self.T_ranges = []
        self.coefficients = []
        for i in range(0, self.num_T_ints):
            T_range = [float(T) for T in lines[2 + 3*i][0:22].split()]
            self.T_ranges.append(T_range)
            coeff_block = lines[3 + 3*i] + lines[4 + 3*i]
            coeffs_raw = [coeff_block[j:j+16] for j in range(0, len(coeff_block), 16)]
            coeffs_raw = coeffs_raw[0:7] + coeffs_raw[8:10]
            coeffs = [float(c.replace('D','e')) for c in coeffs_raw]
            self.coefficients.append(coeffs)
        print(self)

    def __str__(self):
        return(print_str.format(self.species_name, self.source, self.moleculr_wt, \
                ', '.join([str(tuple(T)) for T in self.T_ranges])))

    def _getCoeffs(self, T):
        for i in range(0, self.num_T_ints):
            if T >= self.T_ranges[i][0] and T < self.T_ranges[i][1]:
                return(self.coefficients[i])
        print('{} K is out of valid range(s) for {}!'.format(T, \
                                                                self.species_name))
        raise ValueError
    
    def cp_0(self, T): # J/mol-K
        c = self._getCoeffs(T) # c[0-6] => a1-a7, c[7-8] => b1-b2
        return(self.R*(c[0]*T**(-2) + c[1]*T**(-1) + c[2] + c[3]*T + \
            c[4]*T**2 + c[5]*T**3 + c[6]*T**4))

    def h_0(self, T): # J/mol
        c = self._getCoeffs(T) # c[0-6] => a1-a7, c[7-8] => b1-b2
        return(self.R*T*(-c[0]*T**(-2) + c[1]*math.log(T)/T + c[2] + \
            c[3]*T/2 + c[4]*(T**2)/3 + c[5]*(T**3)/4 + c[6]*(T**4)/5 + c[7]/T))

    def s_0(self, T): # J/mol-K
        c = self._getCoeffs(T) # c[0-6] => a1-a7, c[7-8] => b1-b2
        return(self.R*(-c[0]*(T**(-2))/2 - c[1]*T**(-1) + c[2]*math.log(T) + \
                c[3]*T + c[4]*(T**2)/2 + c[5]*(T**3)/3 + c[6]*(T**4)/4 + c[8]))

    def g_0(self, T): # J/mol
        return(self.h_0(T) - T*self.s_0(T))

    def printState(self, T):
        print('State for {} at {} K:\ncp_0 = {} J/mol-K\nh_0 = {} J/mol\ns_0 = {} J/mol-K\
                \ng_0 = {} J/mol\n'.format(\
                self.species_name, T, self.cp_0(T), self.h_0(T), self.s_0(T), self.g_0(T)))

if __name__ == '__main__':
    Water = Species('H2O(L)')
    Steam = Species('H2O')
    
    test_temp = 300 # K
    Water.printState(test_temp)
    Steam.printState(1500)

    h_0_water = Water.h_0(test_temp)
    print('{} J/mol'.format(h_0_water))
