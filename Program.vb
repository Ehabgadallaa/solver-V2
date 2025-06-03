Imports System
'Imports Microsoft.VisualBasic ' لم نعد نحتاج InputBox، لذا يمكن إزالة هذا السطر أو تركه معطلاً

Module Program

    Sub Main()
        ' تعريف المتغيرات
        Dim A As Integer
        Dim B As Integer
        Dim C As Integer

        ' طلب إدخال قيمة A من المستخدم عبر سطر الأوامر (Console)
        Console.Write("من فضلك، أدخل قيمة لـ A: ") ' Console.Write لعرض النص بدون سطر جديد
        Dim inputA As String = Console.ReadLine() ' قراءة السطر كاملاً من المستخدم

        ' محاولة تحويل النص المدخل إلى عدد صحيح
        If Integer.TryParse(inputA, A) = False Then
            Console.WriteLine("قيمة غير صالحة لـ A. سيتم استخدام 0.")
            A = 0
        End If

        ' طلب إدخال قيمة B من المستخدم عبر سطر الأوامر (Console)
        Console.Write("من فضلك، أدخل قيمة لـ B: ")
        Dim inputB As String = Console.ReadLine()

        ' محاولة تحويل النص المدخل إلى عدد صحيح
        If Integer.TryParse(inputB, B) = False Then
            Console.WriteLine("قيمة غير صالحة لـ B. سيتم استخدام 0.")
            B = 0
        End If

        ' إجراء العملية الحسابية
        C = A + B

        ' طباعة قيمة C على سطر الأوامر (Console)
        Console.WriteLine("C = " & C.ToString())

        ' مهم جداً عشان الشاشة متقفلش بسرعة بعد عرض الناتج
        Console.ReadKey() ' ينتظر ضغط أي مفتاح قبل إغلاق النافذة
    End Sub

End Module