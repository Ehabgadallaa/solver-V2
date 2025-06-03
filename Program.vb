Imports System


    Module Program

    Sub Main()
        ' تعريف المتغيرات وإسناد القيم
        Dim A As Integer = 5
        Dim B As Integer = 6

        ' إجراء العملية الحسابية
        Dim C As Integer = A + B

        ' طباعة قيمة C على سطر الأوامر (Console)
        Console.WriteLine("C= " & C.ToString())

        ' مهم جداً عشان الشاشة متقفلش بسرعة بعد عرض الناتج
        Console.ReadKey() ' ينتظر ضغط أي مفتاح قبل إغلاق النافذة
    End Sub

End Module

