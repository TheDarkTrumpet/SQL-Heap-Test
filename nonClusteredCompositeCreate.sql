CREATE NONCLUSTERED INDEX IX_testTable
    ON dbo.testTable (intColumn, md5);
GO