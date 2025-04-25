USE [Crash Scope DWH]
GO

/****** Object:  Table [dbo].[Dim_Surrounding_Conditions]    Script Date: 4/24/2025 3:19:15 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Dim_Surrounding_Conditions](
	[Surrounding_Conditions_ID_PK_SK] [int] IDENTITY(1,1) NOT NULL,
	[Crash_Record_ID_BK] [nvarchar](255) NULL,
	[WEATHER_CONDITION] [nvarchar](100) NULL,
	[LIGHTING_CONDITION] [nvarchar](100) NULL,
	[SSC] [int] NULL,
	[start_date] [datetime] NULL,
	[end_date] [datetime] NULL,
	[is_current] [bit] NULL,
 CONSTRAINT [PK__Dim_Surr__8654F2D0A9BF42CB] PRIMARY KEY CLUSTERED 
(
	[Surrounding_Conditions_ID_PK_SK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dim_Surrounding_Conditions] ADD  CONSTRAINT [DF__Dim_Surro__start__4316F928]  DEFAULT (getdate()) FOR [start_date]
GO

ALTER TABLE [dbo].[Dim_Surrounding_Conditions] ADD  CONSTRAINT [DF__Dim_Surro__is_cu__440B1D61]  DEFAULT ((1)) FOR [is_current]
GO


