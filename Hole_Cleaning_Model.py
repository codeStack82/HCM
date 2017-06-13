#Python libraries
import sys
import os
import csv
import pyodbc 

#Begin Helper Function Section
#--------------------------------------------#
#1)Print table infomation -> void
def print_Table(table):
    print("Query Results-----------------------")
    for r in table:
        info = ""
        for c in r:
            info += str(c)
            info += " "
        print(info)
#1)End

#End Helper Function Section-----------------#

#Begin Database Connection Func Section
#--------------------------------------------#
#1)CHKShot DB connecton Function
def CHKShot_Execute_Query(chkshot_query):
    try:
        #Create MS SQL conection via ODBC driver
        db = pyodbc.connect("DSN=SQL_R_CHKShot")

        #Create Python cursor (con)
        con = db.cursor() 

        #Execute query
        con.execute(chkshot_query)
        chkshot_data = con.fetchall()

        #Close Connection

        con.close()
        
        return chkshot_data

    except "Query Error":
        print("Query Error!")

#1)End    

#2)Wellview DB connecton Function
def WV_Execute_Query(wv_query):
        #Create MS SQL conection via ODBC driver
        db = pyodbc.connect("DSN=SQL_R_WV") 

        #Create Python cursor (con)
        con = db.cursor() 

        #Execute query
        con.execute(wv_query)
        wv_data = con.fetchall()

        #Close Connection
        con.close()

        return wv_data
      
#2)End

#3)VuMax DB connecton Function
def vmx_Execute_Query(vmx_query):
    try:
        #Create MS SQL conection via ODBC driver
        db = pyodbc.connect(driver='{SQL Server}', server='OKCSQLPRD1021', database='VuMaxDR',
                            uid="Vmx_vumaxadmin",pwd="vumaxadmin",trusted_connection="no")
        #Create Python cursor (con)
        con = db.cursor() 

        #Execute query
        con.execute(vmx_query)
        vmx_data = con.fetchall()

        #Close Connection
        con.close()

        return vmx_data

    except "Query Error":
        print("Query Error!")
        
#3)End

#4)File Read Table Function
def file_Read_Query(file):
    table = ""
    try:
        fh = open(file, "r")
        try:
            table = fh.read()
        finally:
            fh.close()
            return table
    except IOError:
        print("Error: can\'t find file or read data")
#4)

#5)File Write Table Function
def file_Write_Query(table, file_Info):
    try:
        with open(file_Info, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in table:
                writer.writerow(row)
        print("File Saved")
    except IOError:
        print("Error: can\'t find file or read data")
#5)End
#End Database Connection Func Section-------#

#Testing Section--------------------------------------------------------------------#
    #Wellview Table - Test
    #wv_WH_Query = "Select WellIDC, WellName from wvWellHeader where WellIDC = '656388'"
    #wv_Table = WV_Execute_Query(wv_WH_Query)
    #print_Table(wv_Table)

    #VuMax Tables - Test
    #vmx_AW_Query = "Select top 1 * from [dbo].[timeLog657892Wellbore1TimeLog1]"
    #vmx_AW_Table = vmx_Execute_Query(vmx_AW_Query) 
    #print_Table(vmx_AW_Table)

    #CHKShot Table - Test
    #chkshot_Query = """
        #SELECT SVY.DrillingStatus
        # , SVY.PtbMeasuredDepth as Ptb_Md
        # , SVY.PtbInclination as Ptb_Inc
        # , SVY.PtbAzimuth as Ptb_Azm
        # , Round(SVY.AboveBelowPlan,2) as AB_Plan
        # , Round(SVY.LeftRightPlan,2) as LR_Plan
        # , Round(SVY.DogLegSeverity,2) as DLS
        # , Round(SVY.DogLegNeeded,2) as DLN
        #, SVY.WellHeaderID as wellId
        #, Round(planSVY.MeasuredDepth,0) as Plan_TD
        #, Round(((SVY.PtbMeasuredDepth / planSVY.MeasuredDepth) *100),1) as '%Complete'
        #--  , Concat('http://chkshot/Well/', cast(SVY.WellHeaderID as varchar(4))) as wellId
        #FROM chkshot.vw_CurrentWell AS CW with (nolock) 
        #	OUTER APPLY ( 
        #		SELECT TOP 1 DrillingStatus, PtbMeasuredDepth 
        #					, PtbInclination 
        #					, PtbAzimuth 
        #					, AboveBelowPlan , LeftRightPlan 
        #					, DogLegSeverity
        #					, DogLegNeeded 
        #					, WellHeaderID 
        #		FROM chkshot.vw_CHKShot_Moblize_Active_Surveys AS SVY with (nolock) 
        #		WHERE SVY.PropertyNumber = CW.PropertyNumber 
        #		ORDER BY SVY.MeasuredDepth DESC 
        #	) AS SVY 
        #
        #				OUTER APPLY ( 
        #					SELECT TOP 1 MeasuredDepth
        #					FROM [chkshot].[vw_CHKShot_Moblize_WellPlan] AS pSVY with (nolock) 
        #					WHERE pSVY.PropertyNumber = CW.PropertyNumber 
        #					ORDER BY pSVY.MeasuredDepth DESC 
        #				) AS planSVY 
        #
        #
        #           WHERE CW.PropertyNumber = '656388'"""

    #chkshot_Table = CHKShot_Execute_Query(chkshot_Query)
    #print_Table(chkshot_Table)

    #TODO: Need to work on File streams still
    #File Read in Table - Test
    #file_Name = "\High Severity Well List.txt"
    #file_Location  = "V:\Drilling Liaison\Hole Cleaning Charter\HCP Files"
    #file_Info = file_Location + file_Name
    #file_Table = file_Read_Query(file_Info)
    #print("Text File Contents------")
    #print(file_Table)

    #File Write out Table - Test
    #file_Name = "\High Severity Well List-test.txt"
    #file_Location  = "V:\Drilling Liaison\Hole Cleaning Charter\HCP Files"
    #file_Info = file_Location + file_Name
    #file_Write_Query(file_Table, file_Info)
#End Testing Section----------------------------------------------------------------#

#Well Info
well_Dict = {
            'PN':'658840', 
            'Wellbore_NUM':'1',
            'TL_NUM':'2'
            }
#Query not working yet
vmx_q1 = """;WITH RS_AGG AS (
            SELECT
            DATA_INDEX,
            RIG_STATE,
            /*case when RIG_STATE = 0 then 'Rotary Drill'
            when RIG_STATE = 1 then 'Slide Drill'
            when RIG_STATE = 2 then 'In Slips'
            when RIG_STATE = 3 then 'Ream'
            when RIG_STATE = 4 then 'Pump In'
            when RIG_STATE = 5 then 'Rotate In'
            when RIG_STATE = 6 then 'Trip In'
            when RIG_STATE = 7 then 'Back Ream'
            when RIG_STATE = 8 then 'Pump Out'
            when RIG_STATE = 9 then 'Rotate Out'
            when RIG_STATE = 10 then 'Trip Out'
            when RIG_STATE = 11 then 'Rotate and circ'
            when RIG_STATE = 12 then 'Circ'
            when RIG_STATE = 13 then 'Rotate'
            when RIG_STATE = 14 then 'Stationary'
            when RIG_STATE = 16 then 'No Data'
            when RIG_STATE = 17 then 'Packed Off'
            when RIG_STATE = 18 then 'Pressure Testing'
            when RIG_STATE = 19 then 'Auto Slide Drilling'
            when RIG_STATE = 20 then 'Air Drilling' END as 'Rig_State_Name',*/
            case when HDTH - depth <100 and Rig_State in(0,1,3,4,7,8,11,12,19) then 'On Bottom Circ'
            when HDTH - depth >100 and Rig_State in(0,1,3,4,7,8,11,12,19) then 'Off Bottom Circ'
            else 'No Circ'
            END as 'On_Off_Bottom_Circ'""" 
vmx_q2 =" from timeLog" + well_Dict['PN']  + "Wellbore" + well_Dict['Wellbore_NUM'] + "TimeLog" + well_Dict['TL_NUM'] 
vmx_q3 = """),RS_AGG_2 AS ( 
            SELECT 
            tl.DATA_INDEX,
            case
            when RS_AGG.On_Off_Bottom_Circ <> LAG(RS_AGG.On_Off_Bottom_Circ,1) OVER (order by tl.DATA_INDEX)then 1
            else 0
            end as 'NEW_CIRC_STATE' """
vmx_q4 = " from timeLog" + well_Dict['PN']  + "Wellbore" + well_Dict['Wellbore_NUM'] + "TimeLog" + well_Dict['TL_NUM'] + " tl" 
vmx_q5 = """ INNER JOIN RS_AGG on tl.DATA_INDEX = RS_AGG.DATA_INDEX),
            RS_SEQ AS (
            SELECT
            Circ_Sequence,
            COUNT(Circ_Sequence) as Rows_In_Group
            FROM(
            SELECT
            a.DATA_INDEX,
            a.NEW_CIRC_STATE,
            1 + SUM(NEW_CIRC_STATE) OVER(ORDER BY DATA_INDEX ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Circ_Sequence
            FROM (
            SELECT 
            tl.DATA_INDEX,
            case
            when RS_AGG.On_Off_Bottom_Circ <> LAG(RS_AGG.On_Off_Bottom_Circ,1) OVER (order by tl.DATA_INDEX)then 1
            else 0
            end as 'NEW_CIRC_STATE', On_Off_Bottom_Circ"""
vmx_q6 = " from timeLog" + well_Dict['PN']  + "Wellbore" + well_Dict['Wellbore_NUM'] + "TimeLog" + well_Dict['TL_NUM'] + " tl" 
vmx_q7 =""" INNER JOIN RS_AGG on tl.DATA_INDEX = RS_AGG.DATA_INDEX
            )a
            )b
            GROUP BY Circ_Sequence),
            R1 As (
            SELECT
            tl.DATA_INDEX,
            tl.DATETIME,
            tl.depth as 'Bit_Depth',
            tl.HDTH as 'Hole_Depth',
            tl.HDTH - LAG(tl.HDTH,1) OVER (order by tl.DATA_INDEX) as Footage_Made,
            tl.HDTH - LAG(tl.HDTH,1) OVER (order by tl.DATA_INDEX) as Cuttings,
            tl.RPM,
            tl.CIRC,
            tl.ROPAvg,
            tl.RIG_STATE,
            --RS_AGG.Rig_State_Name,
            RS_AGG.On_Off_Bottom_Circ,
            RS_AGG_2.NEW_CIRC_STATE,
            1 + SUM(RS_AGG_2.NEW_CIRC_STATE) OVER(ORDER BY tl.DATA_INDEX ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Circ_Sequence""" 
vmx_q8 =" from timeLog" + well_Dict['PN']  + "Wellbore" + well_Dict['Wellbore_NUM'] + "TimeLog" + well_Dict['TL_NUM'] + " tl" 
vmx_q9 ="""INNER JOIN RS_AGG on tl.DATA_INDEX = RS_AGG.DATA_INDEX
            LEFT JOIN RS_AGG_2 on tl.DATA_INDEX = RS_AGG_2.DATA_INDEX
            )select R1.*, RS_SEQ.Rows_In_Group FROM R1 Inner Join RS_SEQ on RS_SEQ.Circ_Sequence = R1.Circ_Sequence WHERE RS_SEQ.Rows_In_Group > 12 ORDER BY DATA_INDEX"
            ,sep = "", collapse = "")
            ))"""

vmx_query = vmx_q1 + vmx_q2 + vmx_q3 + vmx_q4 + vmx_q5 + vmx_q6 + vmx_q7 + vmx_q8 + vmx_q9
vmx_Table = vmx_Execute_Query(vmx_query)
print_Table(vmx_Table)