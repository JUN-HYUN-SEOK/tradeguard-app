# 파일 수정 스크립트 - 손상된 부분 제거하고 누락된 함수들 추가

with open('trade_guard_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1013번 라인까지만 유지
fixed_lines = lines[:1013]

# 올바른 create_excel_file 함수 종료 + 누락된 함수들 추가
complete_code = '''            
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"엑셀 생성 오류: {e}")
        return None

def create_word_document(results, summary_data):
    """워드 문서 생성 (특이건만 상세 포함)"""
    try:
        doc = Document()
        doc.add_heading('수입신고 RISK 분석 보고서', 0)
        doc.add_paragraph(datetime.datetime.now().strftime("%Y-%m-%d"))
        
        if summary_data:
            doc.add_heading('종합 요약', level=1)
            p = doc.add_paragraph()
            p.add_run(f"전체 신고 건수: {summary_data.get('전체 신고 건수', 0):,} 건").bold = True
            
            if 'Risk분석' in summary_data:
                risk_df = summary_data['Risk분석']
                risk_found = risk_df[risk_df['신고건수'] > 0]
                
                if len(risk_found) > 0:
                    p.add_run(f"\\n\\n⚠️ 발견된 Risk 유형: {len(risk_found)}건").bold = True
                    for _, row in risk_found.iterrows():
                        p.add_run(f"\\n- {row['Risk 유형']}: {row['신고건수']:,} 건 ({row['비율(%)']:.1f}%)")
                else:
                    p.add_run("\\n\\n✅ 특이사항이 발견되지 않았습니다.").bold = True
        
        section_titles = {
            'eight_percent': ('8% 환급 검토', '8% 환급 검토  대상', ['수입신고번호', '세번부호', '관세실행세율', '금액', '거래품명']),
            'zero_risk': ('0% 세율 위험', '0% 세율 위험', ['수입신고번호', '세번부호', '세율구분', '관세실행세율', '거래품명']),
            'tariff_risk': ('세율 위험', '세율 위험(세번부호 불일치)', ['규격1', '세번부호', '세율구분', '거래품명']),
            'price_risk': ('단가 위험', '단가 이상치 (Z-Score)', ['수입신고번호', '규격1', '단가', 'Z-Score', '평균단가']),
            'domestic_tax': ('내국세구분 누락', '내국세구분 누락', ['수입신고번호', '세번부호', '거래품명', '금액']),
            'import_req_risk': ('수입요건 Risk', '수입요건 불일치', ['규격1', '수입신고번호', '법령코드', '발급서류명']),
            'f_rate': ('F세율 적용', 'F세율 적용 건', ['수입신고번호', '세번부호', '세율구분', '세율설명', '거래품명']),
            'fta_opp': ('FTA 기회 발굴', 'FTA 적용 기회', ['수입신고번호', '세번부호', '관세실행세율', '적출국코드', '원산지코드']),
            'low_price': ('저가신고 의심', '저가신고 의심 건', ['수입신고번호', '거래품명', '단가', '금액', '결제통화단위']),
            'currency_inc': ('통화단위 불일치', '통화단위 불일치 건', ['무역거래처상호', '결제통화단위', '수입신고번호', '금액']),
            'country_curr_inc': ('국가별 통화단위 불일치', '국가별 희귀 통화단위 사용', ['무역거래처국가코드', '결제통화단위', '사용비율', '이상치점수']),
            'trade_type': ('특수거래 구분', '특수거래 구분 건', ['수입신고번호', '거래구분', '세번부호', '거래품명', '금액']),
            'free_freight': ('무상운임 누락', '무상운임 누락 의심', ['수입신고번호', '결제방법', '운임', '금액', '거래품명']),
            'usage_rate': ('용도세율 적용', '용도세율 적용 건', ['수입신고번호', '세번부호', '세율구분', '세율설명', '거래품명'])
        }

        has_findings = False
        for key, (title, desc, display_cols) in section_titles.items():
            data =  results.get(key)
            if data is not None and not data.empty:
                has_findings = True
                doc.add_heading(title, level=1)
                doc.add_paragraph(f'총 {len(data):,} 건의 {desc}이(가) 식별되었습니다.')
                
                doc.add_paragraph('📋 상위 5건 샘플:', style='Heading 2')
                sample_data = data.head(5)
                sample_data = format_date_columns(sample_data)
                
                available_cols = [col for col in display_cols if col in sample_data.columns]
                if len(available_cols) == 0:
                    available_cols = sample_data.columns[:5].tolist()
                
                table = doc.add_table(rows=1, cols=len(available_cols))
                table.style = 'Light Grid Accent 1'
                
                header_cells = table.rows[0].cells
                for i, col_name in enumerate(available_cols):
                    header_cells[i].text = col_name
                    header_cells[i].paragraphs[0].runs[0].font.bold = True
                
                for _, row in sample_data.iterrows():
                    row_cells = table.add_row().cells
                    for i, col_name in enumerate(available_cols):
                        value = row.get(col_name, '')
                        if isinstance(value, (int, float)) and not pd.isna(value):
                            if col_name in ['Z-Score', '평균단가', '표준편차', '사용비율', '이상치점수']:
                                row_cells[i].text = f"{value:.2f}"
                            else:
                                row_cells[i].text = f"{value:,.0f}" if value != 0 else "0"
                        else:
                            row_cells[i].text = str(value) if pd.notna(value) else ''
                
                doc.add_paragraph()
        
        if not has_findings:
            doc.add_heading('분석 결과', level=1)
            doc.add_paragraph('✅ 검토가 필요한 특이사항이 발견되지 않았습니다.')
        
        doc.add_paragraph()
        footer = doc.add_paragraph('Generated by 관세법인 우신')
        footer.alignment = 1
        
        doc_output = io.BytesIO()
        doc.save(doc_output)
        doc_output.seek(0)
        return doc_output.getvalue()
    except Exception as e:
        st.error(f"워드 문서 생성 중 오류 발생: {str(e)}")
        return None

def create_html_report(results, summary_data):
    """HTML 보고서 생성 (특이건만 상세 포함)"""
    try:
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>수입신고 RISK 분석 보고서</title>
    <style>
        body {{ font-family: 'Malgun Gothic', 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; font-size: 2.5em; margin-bottom: 10px; border-bottom: 3px solid #667eea; padding-bottom: 15px; }}
        .date {{ text-align: center; color: #7f8c8d; font-size: 1.1em; margin-bottom: 30px; }}
        .summary-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin: 30px 0; box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3); }}
        .metric {{ display: inline-block; background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 8px; margin: 10px; backdrop-filter: blur(10px); }}
        .metric-value {{ font-size: 2em; font-weight: bold; display: block; }}
        .section {{ margin: 40px 0; padding: 25px; background: #f8f9fa; border-radius: 8px; border-left: 5px solid #dc3545; }}
        .section h2 {{ color: #dc3545; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #667eea; color: white; padding: 12px; text-align: left; font-weight: bold; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .no-findings {{ text-align: center; color: #28a745; font-size: 1.3em; padding: 40px; }}
        .footer {{ text-align: center; margin-top: 50px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 수입신고 RISK 분석 보고서</h1>
        <div class="date">{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
        
        <div class="summary-box">
            <h2>종합 요약</h2>
"""
        if summary_data:
            total_count = summary_data.get('전체 신고 건수', 0)
            html_content += f"""
            <div class="metric">
                <span class="metric-value">{total_count:,}</span>
                <span class="metric-label">전체 신고 건수</span>
            </div>
"""
            if 'Risk분석' in summary_data:
                risk_df = summary_data['Risk분석']
                risk_found = risk_df[risk_df['신고건수'] > 0]
                for _, row in risk_found.iterrows():
                    html_content += f"""
            <div class="metric">
                <span class="metric-value">{row['신고건수']:,}</span>
                <span class="metric-label">{row['Risk 유형']} ({row['비율(%)']:.1f}%)</span>
            </div>
"""
        html_content += "</div>"
        
        section_titles = {
            'eight_percent': '8% 환급 검토 대상',
            'zero_risk': '0% 세율 위험',
            'tariff_risk': '세율 위험(세번부호 불일치)',
            'price_risk': '단가 변동성 위험',
            'domestic_tax': '내국세구분 누락',
            'import_req_risk': '수입요건 불일치',
            'f_rate': 'F세율 적용',
            'fta_opp': 'FTA 적용 기회',
            'low_price': '저가신고 의심',
            'currency_inc': '통화단위 불일치',
            'country_curr_inc': '국가별 통화단위 불일치',
            'trade_type': '특수거래 구분',
            'free_freight': '무상운임 누락',
            'usage_rate': '용도세율 적용'
        }
        
        has_findings = False
        for key, desc in section_titles.items():
            data = results.get(key)
            if data is not None and not data.empty:
                has_findings = True
                html_content += f"""
        <div class="section">
            <h2>⚠️ {desc}</h2>
            <p>총 <strong>{len(data):,}</strong> 건의 {desc}이(가) 식별되었습니다.</p>
            <table>
                <thead>
                    <tr>
"""
                sample_data = format_date_columns(data.head(5))
                if len(sample_data) > 0:
                    cols_to_show = list(sample_data.columns[:6])
                    for col in cols_to_show:
                        html_content += f"<th>{col}</th>"
                    html_content += "</tr></thead><tbody>"
                    
                    for _, row in sample_data.iterrows():
                        html_content += "<tr>"
                        for col in cols_to_show:
                            value = row[col]
                            if isinstance(value, (int, float)) and not pd.isna(value):
                                html_content += f"<td>{value:,.2f}</td>"
                            else:
                                html_content += f"<td>{value}</td>"
                        html_content += "</tr>"
                    
                html_content += "</tbody></table></div>"
        
        if not has_findings:
            html_content += '<div class="no-findings">✅ 검토가 필요한 특이사항이 발견되지 않았습니다.</div>'
        
        html_content += """
        <div class="footer">
            <p><strong>Generated by 관세법인 우신</strong></p>
        </div>
    </div>
</body>
</html>
"""
        return html_content
    except Exception as e:
        st.error(f"HTML 보고서 생성 중 오류 발생: {str(e)}")
        return None

def main():
    col1, col2 = st.columns([1, 5])
    with col1:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, 'logo.png')
        
        if os.path.exists(logo_path):
            st.image(logo_path, width=150)
        elif os.path.exists("logo.png"):
            st.image("logo.png", width=150)
    
    with col2:
        st.title("🛡️ TradeGuard (트레이드가드)")
        st.markdown("### 지능형 수입신고 리스크 분석 솔루션")
    
    st.markdown("---")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("made by 전자동")

    uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file is not None:
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            df_original = read_excel_file(uploaded_file, progress_bar, status_text)
            
            if df_original is not None:
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
                st.success(f"📈 데이터 로드 완료: {len(df_original):,}건")
                
                with st.expander("📋 데이터 미리보기"):
                    st.dataframe(df_original.head(10).astype(str), use_container_width=True)
                
                st.sidebar.markdown("### 분석 옵션")
                
                all_options = [
                    "종합 분석", 
                    "8% 환급 검토", "0% 세율 위험", "세율 위험", "단가 위험", "내국세구분", "수입요건 Risk",
                    "F세율 적용", "FTA 기회 발굴", "저가신고 의심", "통화단위 불일치", "국가별 통화단위 불일치", "특수거래 구분", "무상운임 누락", "용도세율 적용"
                ]
                
                analysis_options = st.sidebar.multiselect(
                    "수행할 분석을 선택하세요:",
                    all_options,
                    default=all_options
                )
                
                if st.sidebar.button("🔍 분석 시작", type="primary"):
                    results = {}
                    with st.spinner('분석 중...'):
                        if "종합 분석" in analysis_options: results['summary'] = create_summary_analysis(df_original)
                        if "8% 환급 검토" in analysis_options: results['eight_percent'] = create_eight_percent_refund_analysis(df_original)
                        if "0% 세율 위험" in analysis_options: results['zero_risk'] = create_zero_percent_risk_analysis(df_original)
                        if "세율 위험" in analysis_options: results['tariff_risk'] = create_tariff_risk_analysis(df_original)
                        if "단가 위험" in analysis_options: results['price_risk'] = create_price_risk_analysis(df_original)
                        if "내국세구분" in analysis_options: results['domestic_tax'] = create_domestic_tax_code_analysis(df_original)
                        if "수입요건 Risk" in analysis_options: results['import_req_risk'] = create_import_requirement_risk_analysis(df_original)
                        if "F세율 적용" in analysis_options: results['f_rate'] = create_f_rate_analysis(df_original)
                        if "FTA 기회 발굴" in analysis_options: results['fta_opp'] = create_fta_opportunity_analysis(df_original)
                        if "저가신고 의심" in analysis_options: results['low_price'] = create_low_price_analysis(df_original)
                        if "통화단위 불일치" in analysis_options: results['currency_inc'] = create_currency_consistency_analysis(df_original)
                        if "국가별 통화단위 불일치" in analysis_options: results['country_curr_inc'] = create_country_currency_consistency_analysis(df_original)
                        if "특수거래 구분" in analysis_options: results['trade_type'] = create_trade_type_consistency_analysis(df_original)
                        if "무상운임 누락" in analysis_options: results['free_freight'] = create_free_charge_freight_analysis(df_original)
                        if "용도세율 적용" in analysis_options: results['usage_rate'] = create_usage_rate_analysis(df_original)
                    
                    st.success("분석 완료!")
                    
                    tabs = st.tabs([opt for opt in analysis_options if opt in all_options])
                    
                    key_map = {
                        "종합 분석": 'summary', 
                        "8% 환급 검토": 'eight_percent', 
                        "0% 세율 위험": 'zero_risk',
                        "세율 위험": 'tariff_risk', 
                        "단가 위험": 'price_risk', 
                        "내국세구분": 'domestic_tax',
                        "수입요건 Risk": 'import_req_risk',
                        "F세율 적용": 'f_rate',
                        "FTA 기회 발굴": 'fta_opp',
                        "저가신고 의심": 'low_price',
                        "통화단위 불일치": 'currency_inc',
                        "국가별 통화단위 불일치": 'country_curr_inc',
                        "특수거래 구분": 'trade_type',
                        "무상운임 누락": 'free_freight',
                        "용도세율 적용": 'usage_rate'
                    }

                    for i, tab_name in enumerate(tabs):
                       with tab_name:
                            key = key_map.get(analysis_options[i])
                            data = results.get(key)
                            
                            if key == 'summary' and data:
                                st.markdown("### 📈 종합 분석 대시보드")
                                m1, m2, m3, m4 = st.columns(4)
                                m1.metric("전체 신고 건수", f"{data.get('전체 신고 건수', 0):,}")
                                if 'Risk분석' in data:
                                    risk_df = data['Risk분석']
                                    for idx, row in risk_df.iterrows():
                                        if idx < 3:
                                            (m2 if idx==0 else m3 if idx==1 else m4).metric(
                                                row['Risk 유형'], 
                                                f"{row['신고건수']:,}", 
                                                f"{row['비율(%)']:.1f}%"
                                            )
                                st.markdown("---")
                                
                                c1, c2 = st.columns(2)
                                with c1:
                                    if 'Risk분석' in data:
                                        fig = px.pie(
                                            data['Risk분석'], 
                                            values='신고건수', 
                                            names='Risk 유형', 
                                            title='Risk 유형별 분포', 
                                            hole=0.4,
                                            color_discrete_sequence=px.colors.qualitative.Set3
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                
                                with c2:
                                    if '월별추이' in data:
                                        monthly_df_display = data['월별추이'].copy()
                                        fig = px.line(
                                            monthly_df_display, 
                                            x='수리월', 
                                            y='신고건수', 
                                            title='월별 수입신고 추이', 
                                            markers=True
                                        )
                                        fig.update_xaxes(title_text='수리월 (년-월)', type='category')
                                        fig.update_layout(xaxis_tickangle=-45)
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.info("월별 추이 데이터를 생성할 수 없습니다")

                            elif key == 'price_risk' and isinstance(data, pd.DataFrame) and not data.empty:
                                st.markdown("### 📊 단가 이상치 분포 (Z-Score 기준)")
                                
                                chart_data = data.copy()
                                chart_data[COL_ACCEPTANCE_DATE] = pd.to_numeric(chart_data[COL_ACCEPTANCE_DATE], errors='coerce').fillna(0).astype(int).astype(str)
                                chart_data[COL_ACCEPTANCE_DATE] = pd.to_datetime(chart_data[COL_ACCEPTANCE_DATE], format='%Y%m%d', errors='coerce')
                                
                                fig = px.scatter(
                                    chart_data, 
                                    x=COL_ACCEPTANCE_DATE, 
                                    y=COL_UNIT_PRICE,
                                    color=COL_SPEC_1,
                                    size=chart_data['Z-Score'].abs(),
                                    hover_data=[COL_TRADE_NAME, '평균단가', 'Z-Score'],
                                    title="이상치 산점도 (점 크기: Z-Score 절대값)"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                
                                display_df = format_date_columns(data)
                                st.dataframe(display_df.astype(str), use_container_width=True)

                            elif isinstance(data, pd.DataFrame) and not data.empty:
                                display_df = format_date_columns(data)
                                st.dataframe(display_df.astype(str), use_container_width=True)
                            else:
                                st.info("해당하는 데이터가 없습니다.")

                    st.markdown("---")
                    st.subheader("📥 결과 다운로드")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        excel_data = create_excel_file(df_original, results, results.get('summary', {}))
                        if excel_data:
                            st.download_button("📊 엑셀 보고서", excel_data, f"수입신고분석_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
                            
                    with col2:
                        word_data = create_word_document(results, results.get('summary', {}))
                        if word_data:
                            st.download_button("📄 워드 보고서", word_data, f"수입신고분석_{datetime.datetime.now().strftime('%Y%m%d')}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
                            
                    with col3:
                        html_data = create_html_report(results, results.get('summary', {}))
                        if html_data:
                            st.download_button("🌐 HTML 보고서", html_data, f"수입신고분석_{datetime.datetime.now().strftime('%Y%m%d')}.html", "text/html", use_container_width=True)

if __name__ == "__main__":
    main()
'''

# 최종 파일 작성
with open('trade_guard_app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)
    f.write(complete_code)

print("✅ 파일 수정 완료!")
print(f"- create_excel_file 함수 수정")
print(f"- create_word_document 함수 추가 (특이건만 표시, 상위 5건 표 포함)")
print(f"- create_html_report 함수 추가 (특이건만 표시, 상위 5건 표 포함)")
print(f"- main 함수 추가 (완전한 Streamlit UI)")
