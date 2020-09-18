"""
Parses the borehole from the datas from excel after loaded
This file may not be clear to read,
later needs to be simplified
"""
import re

#use to split
SPLIT_HELPER = re.compile('[(,) :]')

class BoreholeLog:
    """
    Represent single log file
    """

    def _get_header_rows(self):
        """
        Get a single header based on highest hit of hints
        """
        table_header_hints = ['scale', 'depth', 'thickness', 'sampling', 'type', 'classification', 'group', 'symbol', 'spt', 'value', 
                             'n', 'gm', 'cm', 'm', '%', 'layer']
        def check_header_hit(text):
            words = SPLIT_HELPER.split(text)
            for i in words:
                if i in table_header_hints:
                    return 1
                else:
                    return 0
        score_list = []
        row_list = self._data['rows']
        for i in range(len(row_list)):
            score = 0
            for j in range(len(row_list[i])):
                if row_list[i][j].ctype==1:
                    score += check_header_hit(row_list[i][j].value.lower())
            score_list.append(score)
        header_row = 0
        for i in range(len(row_list)):
            if score_list[i] > score_list[header_row]:
                header_row = i
        if score_list[header_row] < 3: #SPT, depth, GI
            #print('- Table not found')
            return None
        # for multi line header
        header_min = header_row
        header_max = header_row
        jump = True
        while(header_min>=0):
            if (score_list[header_min-1]>=score_list[header_row]/2):
                header_min -= 1
                jump = True
            elif jump:
                header_min -= 1
                jump = False
            else:
                break
        header_min += 1
        jump = True
        while(header_max<=len(row_list)):
            if (score_list[header_max+1]>=score_list[header_row]/2):
                header_max += 1
                jump = True
            elif jump:
                header_max += 1
                jump = False
            else:
                break
        header_max -= 1
        merged = self._data['merged_cells']
        for i in merged:
            #amin = amin-1
            (_, amin, _, amax)=i
            #print(header_min, header_max, '-' ,amin, amax, i)
            if (amin <= header_min and amax >= header_min):
                header_min = amin
            if (amin <= header_max and amax >= header_max):
                header_max = amax
        return (header_min, header_max)
    
    def _get_attributes(self):
        """
        Get Attributes info like location, borehole no, ...
        Not properly written now
        All variables are lower case to make it case insensetive
        """
        #@TODO: redefine these later
        def parse_helper(text):
            """
            Function to help parse text
            text in format field: variable
            return (field, variable)
            """
            parts = text.split(':')
            return (parts[0].strip().lower(), parts[1].strip())
        #looks need of proper parser
        # Get attributes from headers
        attributes = {}
        row_list = self._data['rows']
        for i in range(self._header_pos[0]):
            old_text = ''
            expecting = False
            for j in range(len(row_list[i])):
                c_val = str(row_list[i][j].value).strip()
                if c_val:
                    seperator_pos = c_val.find(':')
                    if seperator_pos==-1:
                        if expecting:
                            res = parse_helper(old_text+c_val)
                            attributes[res[0]]=res[1]
                            old_text=''
                            expecting=False
                        else:
                            old_text=c_val
                    else:#check position
                        if seperator_pos==0:
                            old_text+=c_val
                            if len(c_val) > 1:#repeated code @TODO refactor
                                res = parse_helper(old_text)
                                attributes[res[0]]=res[1]
                                old_text=''
                            else:
                                expecting=True
                        else:
                            old_text=c_val
                        #if it ends with next line?
                        if seperator_pos==len(c_val)-1:
                            expecting=True
                        else:
                            res = parse_helper(old_text)
                            attributes[res[0]]=res[1]
                            old_text=''
        return attributes
    
    def _row_list_expand(self):
        """
        Repeat each merged data
        """
        row_list = self._data['rows']
        merged = self._data['merged_cells']
        # Now lets copy values merged cells to every where
        def find_data(clo, rlo, chi, rhi):
            for i in range(rlo, rhi+1):
                for j in range(clo, chi+1):
                    if row_list[i][j].value:
                        return row_list[i][j].value
        for i in merged:
            (clo, rlo, chi, rhi) = i
            for i in range(rlo, rhi+1):
                for j in range(clo, chi+1):
                    row_list[i][j].ctype = 1
                    row_list[i][j].value = find_data(clo, rlo, chi, rhi)

    def _get_map_var_row(self):
        """
        Get variables and their respective columns from header
        """
        # let's get max row size
        max_row_size = 0
        row_list = self._data['rows']
        for i in range(self._header_pos[0], self._header_pos[1]+1):
            row_size = len(row_list[i])
            if max_row_size < row_size:
                max_row_size = row_size
        #
        map_var_row = []
        for j in range(max_row_size):
            map_var_row.append([''])
        for i in range(self._header_pos[1], self._header_pos[0]-1, -1):
            for j in range(max_row_size):
                cval = row_list[i][j].value
                if cval:
                    last_index = len(map_var_row[j])-1
                    if map_var_row[j][last_index].endswith(cval):
                        pass
                    else:
                        if len(map_var_row[j][last_index]):
                            map_var_row[j][last_index]=row_list[i][j].value+' '+map_var_row[j][last_index]
                        else:
                            map_var_row[j][last_index]=row_list[i][j].value
        return map_var_row

    def _get_best_columns(self,rfields,forcedFields=[]):
        """
        Select best comlumn based on constrains
        """
        map_var_row = self._map_var_row
        winners = []
        win_row = 0
        win_count = 0
        win_length = 0 #check only if more than one match(%)
        # Get the best field columnns for requested variables with hints
        for i,d in enumerate(map_var_row):
            this_row_count = 0
            this_word = ''
            for j in d:
                for k in rfields:
                    this_word += j.lower()+' '
                    if k in SPLIT_HELPER.split(j.lower()):
                        this_row_count += 1
            split_words = SPLIT_HELPER.split(this_word)
            this_length = len(split_words)
            found = True
            for k in forcedFields:
                if not k in split_words:
                    found = False
                    break
            if found:
                if this_row_count>win_count:
                    win_row = i
                    win_count = this_row_count
                    winners = [i]
                    win_length = this_length
                elif this_row_count==win_count:
                    if win_length==this_length:
                        winners.append(i)
                    elif win_length>this_length:
                        winners = [i]
        return winners

    def _get_best_cols(self):
        """
        Get column for our requsted variables,
        these are used for further processing
        """
        columns = {}
        columns['spt'] = self._get_best_columns(['spt','n','value'])
        columns['depth'] = self._get_best_columns(['depth','m'], ['depth'])
        columns['sdepth'] = self._get_best_columns(['sampling', 'depth','m'], ['sampling', 'depth'])
        if len(columns['sdepth'])<1:
            columns['sdepth'] = self._get_best_columns(['sampiling', 'depth','m'], ['sampiling', 'depth'])# spelling mistake
        columns['thickness'] = self._get_best_columns(['thickness','m'], ['thickness'])
        columns['classification'] = self._get_best_columns(['classification','soil'], ['classification'])
        columns['gsym'] = self._get_best_columns(['group','symbol'],['group'])
        columns['layer'] = self._get_best_columns(['layer'])
        columns['gamma'] = self._get_best_columns(['g','gm/cm3'])
        columns['wp'] = self._get_best_columns(['w','%'])
        columns['rem'] = self._get_best_columns(['rem'])
        if len(columns['rem'])<1:
            columns['rem'] = self._get_best_columns(['remark'])
        return columns

    def _get_all_data(self, col, ctype):
        """
        Helper function to extract all datas from given column
        """
        # which column and valid data type
        out = []
        row_list=self._data['rows']
        header = self._header_pos
        for i in range(header[1]+1, len(row_list)):
            try:
                cval = row_list[i][col]
                #print(cval.ctype)
                if cval.value:
                    if cval.ctype==ctype:
                        out.append( (cval.value, i) )# and row too
            except:
                pass
        return out

    def _get_spt_data(self):
        """
        Extract SPT data based on best cols
        """
        # For spt
        row_list = self._data['rows']
        header = self._header_pos
        spt_col = self._cols['spt']
        spt_data = []
        if len(spt_col)==1:
            spt_data = self._get_all_data(spt_col[0], 2)
        elif len(spt_col)==3:
            spt_data_0 = self._get_all_data(spt_col[0], 2)
            spt_data_1 = self._get_all_data(spt_col[1], 2)
            spt_data_2 = self._get_all_data(spt_col[2], 2)
            #calculating avg
            for i in range(len(spt_data_0)):
                spt_data.append(spt_data_1[i]+spt_data_2[i]) #ignore first and add other datas
        # lets assume our SPT is always less than 100
        spt_filtered = []
        for (n, row) in spt_data:
            if n<=100:
                spt_filtered.append((n, row))
        spt_data = spt_filtered
        #if(len(spt_data)==0):
        #    helper.fail("No spt data found")
        spt_data.append((0., header[1]+1))
        return spt_data

    def _get_depth_data(self):
        """
        Extract depth data from depth_col and sdepth_col
        """
        row_list = self._data['rows']
        depth_col = self._cols['depth']
        sdepth_col = self._cols['sdepth']
        header = self._header_pos

        # For depth
        depth_data = []
        if len(depth_col)==1:
            depth_data = self._get_all_data(depth_col[0], 2)
        #Use sampling depth datas too if available
        if len(sdepth_col)==1:
            depth_data.extend(self._get_all_data(sdepth_col[0], 2))
        # lets assume our depth is always less than 60
        depth_filtered = []
        for (n, row) in depth_data:
            if n<60.:
                depth_filtered.append((n, row))
        depth_data = depth_filtered
        #if(len(depth_data)==0):
        #    #Proper error later
        #    #helper.fail("No depth data found")
        depth_data.append((0., header[1]+1))
        return depth_data

    def _get_gamma_data(self):
        """
        Read gamma data if available
        """
        row_list = self._data['rows']
        gamma = self._cols['gamma']
        wp = self._cols['wp']        
        header = self._header_pos

        # For gamma
        gamma_data = []
        if len(gamma)==1:
            gamma_data = get_all_data(row_list, header, gamma[0], 2)
        #merge y with wp now if available
        gamma_filtered = []
        if len(wp)==1:
            for v, rv in gamma_data:
                if row_list[rv][wp[0]].ctype==2:
                    w = row_list[rv][wp[0]].value
                    if w:
                        gamma_filtered.append((v/(1+w/100)+1, rv)) #@TODO: fix this formula
                    else:
                        gamma_filtered.append((v, rv))
            gamma_data = gamma_filtered            
        # lets assume our depth is always >1 and <4
        gamma_filtered = []
        for (n, row) in gamma_data:
            if n<4 and n>1:
                gamma_filtered.append((n*9.81, row))
        gamma_data = gamma_filtered
        return gamma_data

    def _get_group_data(self):
        """
        search for soil group
        Read group table automatically
        First gain as much information about it
        """
        row_list = self._data['rows']
        gsym = self._cols['gsym']
        layer = self._cols['layer']
        classification = self._cols['classification']
        
        letters = ['G','S','M','C','O', 'W','P','M','C','L','H', 'I', 'F','T']
        group_data = []
        if len(gsym)==1:
            group_data = self._get_all_data(gsym[0], 1)
        # now get all information from layer and classification
        helper_data = []
        if len(layer)==1:
            helper_data.extend(self._get_all_data(layer[0], 1))
        if len(classification)==1:
            helper_data.extend(self._get_all_data(classification[0], 1))
        #Now try to extract info from helper_data
        for (text, no) in helper_data:
            for i in split_helper.split(text):
                i = i.strip()
                if len(i)==1 or len(i)==2:
                    group_data.append((i, no))
        ## Filter those datas
        group_filtered = []
        for (i, ro) in group_data:
            i = i.upper().strip()
            if len(i)==1:
                i=i+i
            if i[1]=="I": #Why I is it L
                i=i[0]+"L"
            if (i[1] in letters):
                group_filtered.append((i, ro))
        group_data = group_filtered
        #if(len(group_data)==0):
        #    helper.fail("No group data found")
        return group_data

    @staticmethod
    def _get_map_ds(spt_data, depth_data):
        """"
        create interpolated depth vs SPT,
        return updates depth values & (depth vs spt)
        """
        map_d_s = []
        for (a, drow) in depth_data:
            amin = 0
            min_v = 0
            amax = 100
            max_v = 100
            found=False
            for (b, srow) in spt_data:
                if srow==drow:
                    found=True
                    map_d_s.append((a, b))
                    break
                elif srow>amin and srow<drow:
                    amin = srow
                    min_v = b
                elif srow<amax and srow>drow:
                    amax = srow
                    max_v = b
            if not found:
                b = (max_v - min_v)/(amax - amin) * (drow- amin)  + min_v
                map_d_s.append((a, b))
        depth_update = []
        for (b, srow) in spt_data:
            amin = 0
            min_v = 0
            amax = 100
            max_v = 100
            found=False
            for (a, drow) in depth_data:
                if srow==drow:
                    found=True
                    break
                elif drow>amin and drow<srow:
                    amin = drow
                    min_v = a
                elif drow<amax and drow>srow:
                    amax = drow
                    max_v = a                
            if not found:
                a = (max_v - min_v)/(amax - amin) * (srow- amin)  + min_v
                map_d_s.append((a, b))
                depth_update.append((a, srow))
        depth_data.extend(depth_update)
        return(depth_data,map_d_s)

    def _get_rem_data(self, row):
        """
        get additional datas given in comment
        like c and phi which should be manually added
        row: row no to search for,
            merge rows to make it available to all in excel
        rem should be in for mat variable=value seperated by ','
        """
        rem = self._cols['rem']
        out = {}#parse and store here
        if len(rem)>0:
            cell = self._data['rows'][row][rem[0]]
            if cell.ctype==1:
                datas = cell.value.split(',')
                for d_data in datas:
                    var_val = d_data.strip().split('=')
                    if len(var_val)==2:
                        out[var_val[0].strip()]=var_val[1].strip()
        return out

    def _analyse_sheet(self):
        """
        Analyse main part of sheet
        """
        spt_data = self._get_spt_data()
        depth_data = self._get_depth_data()
        depth_data, map_d_s = self._get_map_ds(spt_data, depth_data)
        gamma_data = self._get_gamma_data()
        group_data = self._get_group_data()
        #lets combine them
        all_depths = []
        for i,_ in depth_data:
            if not i in all_depths:
                all_depths.append(i)
        all_depths.remove(0.0)
        all_depths.sort()
        def find_data(depth,data):
            """
            Helper function to search for data,
            here used to find SPT datas
            """
            for (i,j) in data:
                if i==depth:
                    return j
                    
        def find_data_row(depth):
            """
            Find data using row no as info,
            """
            #determine row of data
            row = depth_data[0][1]
            for (data, data_row) in depth_data:
                if data == depth:
                    row = data_row
                    break
            return row
        
        def find_data_by_row(row, table):
            """
            the table should be ordered
            """
            #now search result based on row
            prev_data = table[0][0]
            for (data, data_row) in table:
                if data_row>row:
                    break
                prev_data = data
            return prev_data

        out = []
        for depth in all_depths:
            if depth==0.0:
                continue
            res={'depth': depth}
            row = find_data_row(depth)
            res['spt'] = find_data(depth, map_d_s)
            res['GI'] = find_data_by_row(row, group_data)
            if len(gamma_data)>0:
                res['gamma'] = find_data_by_row(row, gamma_data)
            #Analyse rem data if available
            rem_data = self._get_rem_data(row)
            for data_key in rem_data.keys():
                res[data_key] = rem_data[data_key]
            out.append(res)
        return out

    def __init__(self, data):
        """
        This function determines the position of headers so they can be layer used by other parts
        """
        self._data = data
        self._header_pos = self._get_header_rows()
        self.attributes = self._get_attributes()
        self._row_list_expand()
        self._map_var_row = self._get_map_var_row()
        self._cols = self._get_best_cols()
        self.values = self._analyse_sheet()

if __name__ == "__main__":
    import doctest
    doctest.testmod()