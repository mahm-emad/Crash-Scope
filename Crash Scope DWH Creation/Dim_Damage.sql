USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_Damage]    Script Date: 4/24/2025 4:48:02 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_Damage](
	[Damage_ID_PK_SK] [int] IDENTITY(1,1) NOT NULL,
	[Crash_Record_ID_BK] [nvarchar](255) NULL,
	[FIRST_CRASH_TYPE] [nvarchar](100) NULL,
	[CRASH_TYPE] [nvarchar](100) NULL,
	[PRIM_CONTRIBUTORY_CAUSE] [nvarchar](150) NULL,
	[SEC_CONTRIBUTORY_CAUSE] [nvarchar](150) NULL,
	[DAMAGE] [nvarchar](50) NULL,
	[MOST_SEVERE_INJURY] [nvarchar](100) NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [date] NULL,
	[is_current] [bit] NULL,
 CONSTRAINT [PK__Dim_Dama__DA1F04431BF1B689] PRIMARY KEY CLUSTERED 
(
	[Damage_ID_PK_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_Damage] ADD  CONSTRAINT [DF__Dim_Damag__start__4CA06362]  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_Damage] ADD  CONSTRAINT [DF__Dim_Damag__is_cu__4D94879B]  DEFAULT ((1)) FOR [is_current]
GO


