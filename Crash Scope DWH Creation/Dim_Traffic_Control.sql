USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_Traffic_Control]    Script Date: 4/24/2025 3:20:32 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_Traffic_Control](
	[Traffic_Control_ID_SK_PK] [int] IDENTITY(1,1) NOT NULL,
	[Crash_Record_ID_BK] [nvarchar](255) NULL,
	[TRAFFIC_CONTROL_DEVICE] [nvarchar](100) NULL,
	[DEVICE_CONDITION] [nvarchar](100) NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [date] NULL,
	[is_current] [bit] NULL,
 CONSTRAINT [PK__Dim_Traf__EECD39E0577517B5] PRIMARY KEY CLUSTERED 
(
	[Traffic_Control_ID_SK_PK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_Traffic_Control] ADD  CONSTRAINT [DF__Dim_Traff__start__46E78A0C]  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_Traffic_Control] ADD  CONSTRAINT [DF__Dim_Traff__is_cu__47DBAE45]  DEFAULT ((1)) FOR [is_current]
GO


