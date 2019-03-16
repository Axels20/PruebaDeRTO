Attribute VB_Name = "Módulo1"
Sub Reporte()
Attribute Reporte.VB_ProcData.VB_Invoke_Func = " \n14"
Dim val As Variant
Dim fnum As Long
Dim rng As Range

    If ActiveSheet.Shapes.Range(Array("ACUMCON")).Visible = msoFalse And ActiveSheet.Shapes.Range(Array("ACTUALCON")).Visible = msoTrue Then

        Sheets.Add After:=ActiveSheet
        Sheets("Hoja2").Select
        Sheets("Hoja2").Name = "Reporte de Ventas Acumuladas"
        
        'Sheets("Reporte de Ventas Acumuladas").Select
        'Range("A7").Select
        'Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks:=False, Transpose:=False
        
        Worksheets("Reporte de Ventas Acumuladas").Range("A1").FormulaR1C1 = "NOMBRE DEL REPORTE: VENTAS ACUMULADAS"
        Worksheets("Reporte de Ventas Acumuladas").Range("A2").FormulaR1C1 = "FECHA DE EJECUCIÓN: " & Format(Now(), "mm/dd/yyyy")
        Worksheets("Reporte de Ventas Acumuladas").Range("A3").FormulaR1C1 = "CANTIDAD DE REGISTROS: " & fnum
        'Worksheets("Reporte de Ventas Acumuladas").Range("A7").AutoFilter
        
        MsgBox "Reporte Acumulado"
    Else
    
        Set NewSheet = Sheets.Add
        With NewSheet
            .Name = "Reporte de Ventas Acumuladas"
        End With
        
        Worksheets("Reporte de Ventas Acumuladas").Range("A1").FormulaR1C1 = "NOMBRE DEL REPORTE: VENTAS ACUMULADAS"
        Worksheets("Reporte de Ventas Acumuladas").Range("A2").FormulaR1C1 = "FECHA DE EJECUCIÓN: " & Format(Now(), "mm/dd/yyyy")
        Worksheets("Reporte de Ventas Acumuladas").Range("A3").FormulaR1C1 = "CANTIDAD DE REGISTROS: " & fnum
        
        Sheets("Grid").Select
        Range("Y9").Select
        Range(Selection, ActiveCell.End(xlDown).End(xlDown).End(xlToRight)).Select
        'Range(Selection, Selection.End(xlToRight)).Select
        'Range(Selection, Selection.End(xlDown)).Select
        Selection.Copy
        
        Sheets("Reporte de Ventas Acumuladas").Select
        Range("A7").Select
        Selection.PasteSpecial Paste:=xlPasteAllUsingSourceTheme, Operation:=xlNone _
        , SkipBlanks:=False, Transpose:=False
        Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
        
        val = 0
        Set rng = Sheets("Reporte de Ventas Acumuladas").Range("A8", Sheets("Reporte de Ventas Acumuladas").Range("A8").End(xlDown))
        fnum = Application.Match(val, rng, 0)
        fnum = fnum
        
        MsgBox fnum
        
        'Rows(fnum & fnum).Select
        'Range(Selection, Selection.End(xlDown)).Select
        'Range(Selection, Selection.End(xlDown)).Select
        'Selection.Delete Shift:=xlUp
        
        'Sheets("Reporte de Ventas Acumuladas").Select
        'Application.CutCopyMode = False
        'Sheets("Reporte de Ventas Acumuladas").Move
        
        MsgBox "Reporte Semanal"
    End If
    
End Sub

Sub Macro3()
Attribute Macro3.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro3 Macro
'

'
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Range(Selection, Selection.End(xlDown)).Select
    ActiveWindow.SmallScroll Down:=9
    Selection.Copy
    Sheets.Add After:=ActiveSheet
    Range("A10").Select
    Range("A10").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    Columns("A:N").Select
    Columns("A:N").EntireColumn.AutoFit
    Range("A12").Select
End Sub
Sub Macro4()
Attribute Macro4.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro4 Macro
'

'
    Workbooks.Add
    Sheets("Hoja1").Select
    Sheets("Hoja1").Name = "Ventas Acumuladas"
    ActiveCell.FormulaR1C1 = "Nom"
    Windows("MOCKUP_Reportes.xlsm").Activate
    Windows("Libro2").Activate
    ActiveCell.FormulaR1C1 = ""
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "NOMBRE DEL REPORTE: Reporte de Ventas Acumuladas"
    Range("A2").Select
End Sub
Sub Macro5()
Attribute Macro5.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro5 Macro
'

'
    Range("Y9").Select
    ActiveWindow.SmallScroll Down:=-6
    Range("Y9").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.Copy
    Windows("Libro2").Activate
    Range("A6").Select
    Windows("MOCKUP_Reportes.xlsm").Activate
    Selection.Copy
    Windows("Libro2").Activate
    Windows("MOCKUP_Reportes.xlsm").Activate
    ActiveWindow.SmallScroll Down:=-24
End Sub
Sub Macro6()
Attribute Macro6.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro6 Macro
'

'
    Sheets.Add After:=ActiveSheet
    Sheets("Hoja2").Select
    Sheets("Hoja2").Name = "Reporte de Ventas Acumuladas"
    Sheets("Grid").Select
    Range("Y9").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.Copy
    Sheets("Reporte de Ventas Acumuladas").Select
    Range("A7").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    Sheets("Grid").Select
    ActiveWindow.SmallScroll Down:=-132
    Sheets("Reporte de Ventas Acumuladas").Select
    Cells.Select
    Application.CutCopyMode = False
    Selection.ClearContents
    Sheets("Grid").Select
    Range("Y9").Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlToRight)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Range(Selection, Selection.End(xlDown)).Select
    Selection.Copy
    Sheets("Reporte de Ventas Acumuladas").Select
    Range("A7").Select
    Selection.PasteSpecial Paste:=xlPasteAllUsingSourceTheme, Operation:=xlNone _
        , SkipBlanks:=False, Transpose:=False
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
    Columns("A:N").Select
    Columns("A:N").EntireColumn.AutoFit
    Columns("A:N").EntireColumn.AutoFit
    Columns("A:N").EntireColumn.AutoFit
End Sub
Sub Macro7()
Attribute Macro7.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro7 Macro
'

'
    Sheets("Reporte de Ventas Acumuladas").Select
    Application.CutCopyMode = False
    Sheets("Reporte de Ventas Acumuladas").Move
End Sub
